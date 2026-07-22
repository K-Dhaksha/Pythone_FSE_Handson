from typing import Optional

from pydantic import BaseModel, EmailStr


# ==========================
# Authentication Schemas
# ==========================

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================
# Course Schemas
# ==========================

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    class Config:
        from_attributes = True


# ==========================
# Department Schema
# ==========================

class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    budget: float

    class Config:
        from_attributes = True


# ==========================
# Student Schema
# ==========================

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int
    enrollment_year: int

    class Config:
        from_attributes = True


# ==========================
# Enrollment Schema
# ==========================

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: Optional[str] = None

    class Config:
        from_attributes = True