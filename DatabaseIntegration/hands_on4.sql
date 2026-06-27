use college_db;
EXPLAIN
SELECT s.first_name, s.last_name, c.course_name FROM 
enrollments e   JOIN students s 
ON s.student_id = e.student_id   
JOIN courses c ON c.course_id = 
e.course_id   WHERE s.enrollment_year = 2022;

/* EXPLAIN RESULTS
[
  {
    "id": "1",
    "select_type": "SIMPLE",
    "table": "s",
    "partitions": null,
    "type": "ALL",
    "possible_keys": "PRIMARY",
    "key": null,
    "key_len": null,
    "ref": null,
    "rows": "10",
    "filtered": 10,
    "Extra": "Using where"
  },
  {
    "id": "1",
    "select_type": "SIMPLE",
    "table": "e",
    "partitions": null,
    "type": "ref",
    "possible_keys": "student_id,course_id",
    "key": "student_id",
    "key_len": "5",
    "ref": "college_db.s.student_id",
    "rows": "1",
    "filtered": 100,
    "Extra": "Using where"
  },
  {
    "id": "1",
    "select_type": "SIMPLE",
    "table": "c",
    "partitions": null,
    "type": "eq_ref",
    "possible_keys": "PRIMARY",
    "key": "PRIMARY",
    "key_len": "4",
    "ref": "college_db.e.course_id",
    "rows": "1",
    "filtered": 100,
    "Extra": null
  }
]
*/

/*
Question 49:

The EXPLAIN output shows a Full Table Scan on the students table (alias s).
This is indicated by the value 'ALL' in the type column.

*/

/*
Question 50:

Estimated rows examined according to the EXPLAIN output:

students (s): 10 rows
enrollments (e): 1 row
courses (c): 1 row

This indicates that MySQL estimates it will examine 10 rows from the
students table, 1 row from the enrollments table, and 1 row from the
courses table while executing the query.
*/

create INDEX idx_students_enrollment_year
on students(enrollment_year);

CREATE UNIQUE INDEX idx_enrollment_unique
ON enrollments(student_id, course_id);

CREATE INDEX idx_course_code
ON courses(course_code);

EXPLAIN
SELECT s.first_name,
       s.last_name,
       c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

/*
[
  {
    "id": "1",
    "select_type": "SIMPLE",
    "table": "e",
    "partitions": null,
    "type": "ALL",
    "possible_keys": "student_id,course_id",
    "key": null,
    "key_len": null,
    "ref": null,
    "rows": "11",
    "filtered": 100,
    "Extra": "Using where"
  },
  {
    "id": "1",
    "select_type": "SIMPLE",
    "table": "s",
    "partitions": null,
    "type": "eq_ref",
    "possible_keys": "PRIMARY,idx_students_enrollment_year",
    "key": "PRIMARY",
    "key_len": "4",
    "ref": "college_db.e.student_id",
    "rows": "1",
    "filtered": 50,
    "Extra": "Using where"
  },
  {
    "id": "1",
    "select_type": "SIMPLE",
    "table": "c",
    "partitions": null,
    "type": "eq_ref",
    "possible_keys": "PRIMARY",
    "key": "PRIMARY",
    "key_len": "4",
    "ref": "college_db.e.course_id",
    "rows": "1",
    "filtered": 100,
    "Extra": null
  }
]
*/

/*
After creating the indexes and re-running EXPLAIN, the query plan changed.

In the baseline plan, MySQL performed a Full Table Scan (type = ALL)
on the students table. After indexing, the optimizer changed the join
order and now starts with the enrollments table.

The students and courses tables are accessed using eq_ref joins through
their PRIMARY KEY indexes. Although the index
idx_students_enrollment_year is available, MySQL does not use it because
the tables are very small and a different execution plan is estimated to
be more efficient.

Therefore, the query plan changed, but an Index Scan on
idx_students_enrollment_year was not chosen by the optimizer.
*/