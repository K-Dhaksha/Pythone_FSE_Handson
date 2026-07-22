from typing import Optional

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Response,
    BackgroundTasks,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db
from models import Base, Course
from schemas import CourseCreate, CourseUpdate, CourseResponse


app = FastAPI(
    title="Course Management API",
    description="REST API for Course Management using FastAPI",
    version="1.0",
    contact={
        "name": "Dhakshina",
        "email": "admin@college.edu"
    }
)

# ----------------------------------------------------
# API VERSIONING
#
# URL Versioning:
# /api/v1/courses/
#
# Another common approach is Header Versioning:
# Accept: application/vnd.api+json;version=1
# ----------------------------------------------------


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "API running"}


students = []
enrollments = []


def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")


# =====================================================
# COURSES
# =====================================================

@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create Course",
    response_description="Returns the created course"
)
async def create_course(
    response: Response,
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    new_course = Course(**course.model_dump())

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    response.headers["Location"] = (
        f"/api/v1/courses/{new_course.id}"
    )

    return new_course


@app.get(
    "/api/v1/courses/",
    tags=["Courses"]
)
async def get_courses(
    page: int = 1,
    page_size: int = 2,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Course)

    if department_id:
        query = query.where(
            Course.department_id == department_id
        )

    result = await db.execute(query)

    courses = result.scalars().all()

    if search:
        courses = [
            c for c in courses
            if search.lower() in c.name.lower()
            or search.lower() in c.code.lower()
        ]

    total = len(courses)

    start = (page - 1) * page_size
    end = start + page_size

    return {

        "count": total,

        "next":
        f"/api/v1/courses/?page={page+1}&page_size={page_size}"
        if end < total else None,

        "previous":
        f"/api/v1/courses/?page={page-1}&page_size={page_size}"
        if page > 1 else None,

        "results": courses[start:end]

    }


@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(

            status_code=404,

            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Course with id {course_id} does not exist",
                    "field": None
                }
            }

        )

    return course


@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    updated: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(

            status_code=404,

            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Course with id {course_id} does not exist",
                    "field": None
                }
            }

        )

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)

    return course


@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def patch_course(
    course_id: int,
    updated: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(

            status_code=404,

            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Course with id {course_id} does not exist",
                    "field": None
                }
            }

        )

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(course, key, value)

    await db.commit()
    await db.refresh(course)

    return course


@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(

            status_code=404,

            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Course with id {course_id} does not exist",
                    "field": None
                }
            }

        )

    await db.delete(course)
    await db.commit()

    return Response(status_code=204)


@app.get(
    "/api/v1/courses/{course_id}/students",
    tags=["Courses"]
)
async def course_students(course_id: int):

    return {

        "course_id": course_id,

        "students": [

            {"id": 1, "name": "Alice"},

            {"id": 2, "name": "Bob"}

        ]

    }


# =====================================================
# STUDENTS
# =====================================================
# =====================================================
# STUDENTS
# =====================================================

@app.get(
    "/api/v1/students/",
    tags=["Students"]
)
async def get_students():
    return students


@app.post(
    "/api/v1/students/",
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
async def create_student(
    response: Response,
    student: dict
):

    students.append(student)

    response.headers["Location"] = (
        f"/api/v1/students/{len(students)}"
    )

    return student


@app.put(
    "/api/v1/students/{student_id}",
    tags=["Students"]
)
async def update_student(student_id: int):

    return {
        "message": f"Student {student_id} updated"
    }


@app.patch(
    "/api/v1/students/{student_id}",
    tags=["Students"]
)
async def patch_student(student_id: int):

    return {
        "message": f"Student {student_id} partially updated"
    }


@app.delete(
    "/api/v1/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"]
)
async def delete_student(student_id: int):

    return Response(status_code=204)


# =====================================================
# ENROLLMENTS
# =====================================================

@app.get(
    "/api/v1/enrollments/",
    tags=["Enrollments"]
)
async def get_enrollments():

    return enrollments


@app.post(
    "/api/v1/enrollments/",
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    response: Response,
    enrollment: dict,
    background_tasks: BackgroundTasks
):

    enrollments.append(enrollment)

    background_tasks.add_task(
        send_confirmation_email,
        enrollment["student_email"]
    )

    response.headers["Location"] = (
        f"/api/v1/enrollments/{len(enrollments)}"
    )

    return enrollment


@app.put(
    "/api/v1/enrollments/{enrollment_id}",
    tags=["Enrollments"]
)
async def update_enrollment(enrollment_id: int):

    return {
        "message": f"Enrollment {enrollment_id} updated"
    }


@app.patch(
    "/api/v1/enrollments/{enrollment_id}",
    tags=["Enrollments"]
)
async def patch_enrollment(enrollment_id: int):

    return {
        "message": f"Enrollment {enrollment_id} partially updated"
    }


@app.delete(
    "/api/v1/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(enrollment_id: int):

    return Response(status_code=204)