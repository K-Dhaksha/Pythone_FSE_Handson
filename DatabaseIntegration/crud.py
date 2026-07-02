from sqlalchemy.orm import sessionmaker
from models import engine, Department, Student, Course, Enrollment

Session = sessionmaker(bind=engine)
session = Session()

# Create 3 departments
dept1 = Department(dept_name='Computer Science', hod_name='Dr. Ramesh Kumar', budget=850000)
dept2 = Department(dept_name="Electronics and Communication",hod_name="Dr.Helman", budget=90000) # fill in
dept3 = Department(dept_name="Information Technology",hod_name="Dr.Selvi", budget=70000) # fill in

# Add and commit
session.add_all([dept1, dept2, dept3])
session.commit()

student1 = Student(
    first_name='Arjun',
    last_name='Mehta',
    email='arjun@college.edu',
    department_id=dept1.department_id,
    enrollment_year=2022
)
student2 = Student(
    first_name='Heeseung',
    last_name='Lee',
    email='evan@college.edu',
    department_id=dept1.department_id,
    enrollment_year=2021
)
student3 = Student(
    first_name='Dhanishka',
    last_name='Mehta',
    email='dhan@college.edu',
    department_id=dept2.department_id,
    enrollment_year=2023
)
student4 = Student(
    first_name='Jeonghan',
    last_name='Yoon',
    email='yoonzino@college.edu',
    department_id=dept3.department_id,
    enrollment_year=2020
)
student5 = Student(
    first_name='Max',
    last_name='Witch',
    email='witchymax@college.edu',
    department_id=dept3.department_id,
    enrollment_year=2020
)


session.add_all([student1,student2,student3,student4,student5])
session.commit()


course1 = Course(
    course_name='Data Structures', 
    course_code='CS101', credits=4, 
    department_id=dept1.department_id
)
course2 = Course(
    course_name='Digital Signal Processing', 
    course_code='EC102', credits=4, 
    department_id=dept2.department_id
)
course3 = Course(
    course_name='Java', 
    course_code='IT104', credits=4, 
    department_id=dept3.department_id
)

session.add_all([course1, course2,course3])
session.commit()


from datetime import date
enroll1 = Enrollment(
    student_id=student1.student_id, course_id=course1.course_id, 
    enrollment_date=date.today()
)
enroll2= Enrollment(
    student_id=student3.student_id, course_id=course2.course_id, 
    enrollment_date=date.today()
)
enroll3 = Enrollment(
    student_id=student5.student_id, course_id=course3.course_id, 
    enrollment_date=date.today()
)
session.add_all([enroll1,enroll2,enroll3])
session.commit()

students = session.query(Student).join(Department).filter(Department.dept_name == 'Computer Science').all()

enrollments = session.query(Enrollment).all()
for e in enrollments:
    print(e.student.first_name, e.course.course_name)


student = session.query(Student).filter(Student.email == 'evan@college.edu').first()
student.enrollment_year = 2023
session.commit()



enrollment = session.query(Enrollment).filter(Enrollment.enrollment_id == 1).first()
session.delete(enrollment)
session.commit()

from sqlalchemy.orm import joinedload

# AFTER (with joinedload)
enrollments = session.query(Enrollment).options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
).all()

for e in enrollments:
    print(e.student.first_name, e.course.course_name)

# WITHOUT joinedload: 7 queries for 3 enrollments
# WITH joinedload: 1 query for all enrollments
# ==========================================
# N+1 PROBLEM ANALYSIS
# ==========================================
# WITHOUT joinedload:
# - 1 query to fetch all enrollments
# - 1 query per enrollment to fetch student
# - 1 query per enrollment to fetch course
#
# WITH joinedload (eager loading):
# - 1 query with JOINs fetches everything
# - Total: 1 query regardless of data size
# ==========================================