use college_db;
--Undoing all the changes done in hands_on1.sql
ALTER TABLE departments
CHANGE head_of_department hod_name VARCHAR(100);

-- departments
INSERT INTO departments (dept_name, hod_name, budget) VALUES
  ('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
  ('Electronics', 'Dr. Priya Nair', 620000.00),
  ('Mechanical', 'Dr. Suresh Iyer', 540000.00),
  ('Civil', 'Dr. Ananya Sharma', 430000.00);-- students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, 
enrollment_year) VALUES
  ('Arjun',  'Mehta',    'arjun.mehta@college.edu',    '2003-04-12', 1, 2022),
  ('Priya',  'Suresh',   'priya.suresh@college.edu',   '2003-07-25', 1, 2022),
  ('Rohan',  'Verma',    'rohan.verma@college.edu',    '2002-11-08', 2, 2021),
  ('Sneha',  'Patel',    'sneha.patel@college.edu',    '2004-01-30', 3, 2023),
  ('Vikram', 'Das',      'vikram.das@college.edu',     '2003-09-14', 1, 2022),
  ('Kavya',  'Menon',    'kavya.menon@college.edu',    '2002-05-17', 2, 2021),
  ('Aditya', 'Singh',    'aditya.singh@college.edu',   '2004-03-22', 4, 2023),
  ('Deepika','Rao',      'deepika.rao@college.edu',    '2003-08-09', 1, 2022);-- courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
  ('Data Structures & Algorithms', 'CS101', 4, 1),
  ('Database Management Systems',  'CS102', 3, 1),
  ('Object Oriented Programming',  'CS103', 4, 1),
  ('Circuit Theory',               'EC101', 3, 2),
  ('Thermodynamics',               'ME101', 3, 3);-- enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
  (1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
  (2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
  (3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
  (5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
  (6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
  (8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');

-- professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
  ('Dr. Anand Krishnan',  'anand.k@college.edu',   1, 95000.00),
  ('Dr. Meena Pillai',    'meena.p@college.edu',   1, 88000.00),
  ('Dr. Sunil Rajan',     'sunil.r@college.edu',   2, 82000.00),
  ('Dr. Latha Gopal',     'latha.g@college.edu',   3, 79000.00),
  ('Dr. Kartik Bose',     'kartik.b@college.edu',  4, 76000.00);

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, 
enrollment_year) VALUES
  ('Kaz',  'Brekker',    'kaz.brekker@college.edu',    '2003-05-11', 1, 2022),
  ('Inej',  'Ghaffa',   'inej.ghaffa@college.edu',   '2003-08-20', 1, 2022);


Update enrollments set grade='B' where student_id=5 and course_id=1;
SELECT * FROM enrollments WHERE grade IS NULL;
Delete from enrollments where grade is NULL;
SELECT COUNT(*) FROM enrollments;
SELECT * FROM enrollments WHERE grade IS NULL;
SELECT * FROM enrollments
WHERE student_id = 5 AND course_id = 1;



select * from students where enrollment_year="2022" order by last_name;
select * from courses where credits>3 order by credits desc;
select * from professors where salary between 80000 and 95000;
select * from students where email like "%@college.edu";
select enrollment_year, count(*) from students group by enrollment_year;


select concat(first_name,' ',last_name) as full_name, dept_name from students s inner join departments d on d.department_id=s.department_id;
select s.student_id, c.course_id, enrollment_date, grade, first_name, course_name from enrollments e inner join courses c on e.course_id=c.course_id inner join students s on s.student_id=e.student_id group by course_id

select * from students s left join enrollments e on s.student_id=e.student_id where course_id is NULL;
select c.course_id, course_code, course_name, count(e.enrollment_id) from courses c left join enrollments e on c.course_id=e.course_id group by course_id;
select dept_name, prof_name, salary from departments d left join professors p on d.department_id=p.department_id;

select course_name, count(e.enrollment_id) as enrollment_count from courses c left join enrollments e on c.course_id=e.course_id group by c.course_id;

select dept_name, round(avg(salary),2) from departments d inner join professors p on d.department_id=p.department_id group by d.department_id;

select department_id, dept_name from departments where budget>600000;
select grade, count(grade) as grade_distribution from enrollments e inner join courses c on e.course_id=c.course_id where course_code="CS101" group by grade;

select dept_name 
from departments d
join courses c on d.department_id = c.department_id
join enrollments e on c.course_id = e.course_id
group by d.department_id having count(e.student_id)>2;