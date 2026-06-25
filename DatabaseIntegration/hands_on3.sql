use college_db;

select first_name, last_name, count(*) from students s
join enrollments e on s.student_id=e.student_id
group by s.student_id 
having count(*)>(
select avg(enr_count) from (
    select student_id, count(*) as enr_count
    from enrollments 
    group by student_id
) as counts
);

select course_id, course_name from courses c 
where not exists (
    select 1 from enrollments e
    where e.course_id= c.course_id and grade not in ('A')
);

select d.department_id, dept_name, prof_name from departments d
join professors p
on p.department_id=d.department_id
where p.salary=(
    select Max(salary) 
    from professors p2 where p2.department_id=p.department_id
);


select d.department_id, dept_name, asal from departments d
join (
select department_id, avg(salary) as asal from professors p
group by department_id
) as avgtab on d.department_id=avgtab.department_id
where asal>85000;

create view vw_student_enrollment_summary as 
select concat(first_name,' ',last_name) as full_name, dept_name, count(*) as no_of_courses,
avg( 
    case
    WHEN grade = 'A' THEN 4
    WHEN grade = 'B' THEN 3
    WHEN grade = 'C' THEN 2
    WHEN grade = 'D' THEN 1
    WHEN grade = 'F' THEN 0
    end
) as gpa
from departments d
join students s on d.department_id=s.department_id
join enrollments e on s.student_id=e.student_id
group by s.student_id;

select * from vw_student_enrollment_summary;

create view vw_course_stats as
select course_name, course_code,
avg( 
    case
    WHEN grade = 'A' THEN 4
    WHEN grade = 'B' THEN 3
    WHEN grade = 'C' THEN 2
    WHEN grade = 'D' THEN 1
    WHEN grade = 'F' THEN 0
    end
) as gpa,
count(*) as total_enrollments 
from courses c
join enrollments e
on c.course_id=e.course_id
group by c.course_id;

select * from vw_course_stats;
select * from vw_student_enrollment_summary where gpa>3;

update vw_student_enrollment_summary
set dept_name = 'Electronics'
where full_name = 'Arjun Mehta';

-- WHY MULTI-TABLE VIEWS ARE NOT UPDATABLE:
-- 
-- 1. This view joins 3 tables (departments, students, enrollments)
--    MySQL cannot determine which base table to update when
--    multiple tables are involved.
--
-- 2. Columns like full_name are derived (CONCAT) so MySQL
--    cannot reverse it back to first_name and last_name.
--
-- 3. Aggregated columns like gpa and no_of_courses are
--    calculated values -- they don't exist in any real table
--    so they cannot be updated directly.

DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

create VIEW vw_student_enrollment_summary as
select * from students
where department_id = 1
with check option;

UPDATE vw_student_enrollment_summary
SET department_id = 2
WHERE student_id = 1;

UPDATE vw_student_enrollment_summary
SET enrollment_year = 2023
WHERE student_id = 1;

-- WITH CHECK OPTION ANALYSIS
--
-- View only shows students where department_id = 1
-- WITH CHECK OPTION prevents any update that would
-- make a row disappear from the view.
--

create procedure sp_enroll_students(
    IN student_id1 int,
    IN course_id2 int,
    IN enrollment_date1 date
)
begin
if exists (
    select 1 from enrollments
    where student_id=student_id1 and course_id=course_id2

)
then 
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Student already enrolled in this course!';
else
insert into enrollments  (student_id,course_id,enrollment_date) 
values (student_id1, course_id2,enrollment_date1);
END IF;
END 


CALL sp_enroll_students(1, 3, '2024-01-01');

CREATE TABLE department_transfer_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date DATETIME
);

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_old_dept_id INT,
    IN p_new_dept_id INT
)
BEGIN
    -- Declare exit handler for errors
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transfer failed! Transaction rolled back.';
    END;

    -- Start transaction
    START TRANSACTION;

    update students 
    set department_id=p_new_dept_id;

    insert into department_transfer_log(
        student_id, old_department_id, new_department_id)
    values(p_student_id, p_old_dept_id,p_new_dept_id);

    -- Step 2: INSERT into department_transfer_log
    -- your code here

    -- If both succeed
    COMMIT;
END

CALL sp_transfer_student(1, 1, 2);

CALL sp_transfer_student(1, 1, 99);
SELECT student_id, department_id FROM students WHERE student_id = 1;
SELECT * FROM department_transfer_log;


-- Start transaction
START TRANSACTION;

-- Insert first enrollment
INSERT INTO enrollments (student_id, course_id, enrollment_date)
VALUES (3, 2, '2024-01-01');

-- Set savepoint after first insert
SAVEPOINT after_first_insert;

-- Insert second enrollment (invalid -- student 99 doesn't exist)
INSERT INTO enrollments (student_id, course_id, enrollment_date)
VALUES (99, 2, '2024-01-01');

-- Second insert failed so rollback to savepoint
ROLLBACK TO SAVEPOINT after_first_insert;

-- Commit -- only first insert is saved
COMMIT;