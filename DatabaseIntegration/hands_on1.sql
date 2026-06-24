-- Create and select the database
CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- departments must come first (other tables reference it)
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name     VARCHAR(100) NOT NULL,
    hod_name      VARCHAR(100),
    budget        DECIMAL(12,2)
);

CREATE TABLE students (
    student_id      INT PRIMARY KEY AUTO_INCREMENT,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth   DATE,
    department_id   INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id   INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits     INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id   INT PRIMARY KEY AUTO_INCREMENT,
    student_id      INT,
    course_id       INT,
    enrollment_date DATE,
    grade           CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

CREATE TABLE professors (s
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE,
    department_id INT,
    salary       DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


-- NORMALISATION ANALYSIS
-- 
-- 1NF: All columns in every table hold atomic values.
--      There are no multi-valued fields exist. Our schema stores only one value per cell.
--
-- 2NF: The enrollments table has a composite candidate key (student_id + course_id).
--      All the non-key columns ( like enrollment_date, grade) depend on BOTH columns together.
--      grade depends on both the student and the course
--      enrollment_date depends on both the student and when the enrolled in the course
--      Hence, no partial dependency exists. The schema satisfies 2NF.
--
-- 3NF: There are no transitive dependencies.
--      If we stored dept_name in students, we would create
--      student_id → department_id → dept_name (creating a transitive dependency).
--      Instead dept_name lives in the departments table, so it is directly dependent
--      on department_id (its own primary key). Schema satisfies 3NF.


ALTER TABLE students ADD COLUMN phone_number VARCHAR(100);
Alter table courses add column max_seats INT Default 60;
Alter table enrollments add constraint check (grade in ('A', 'B','C','D','E','F') or grade is NULL);
Alter table departments change hod_name head_of_department VARCHAR(100);
Alter table students drop column phone_number;

DESCRIBE students;
Describe courses;
Describe enrollments;
Describe departments;
