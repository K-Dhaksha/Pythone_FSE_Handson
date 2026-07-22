from datetime import timedelta
from database import engine, get_db
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Response,
    BackgroundTasks
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db
from models import Base, Course, User
from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    UserCreate,
    Token
)

from security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)


app = FastAPI(
    title="Course Management API",
    description="Course Management API with JWT Authentication",
    version="1.0",
    contact={
        "name": "Dhakshina",
        "email": "admin@college.edu"
    }
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {
        "message": "API running"
    }


students = []
enrollments = []


def send_confirmation_email(student_email: str):
    print(
        f"Sending confirmation to {student_email}"
    )


# ---------------------------------------------------------
# OAuth2 Authorization Code Flow
#
# OAuth2 uses an Authorization Server where users
# log in and grant permission before an access token
# is issued.
#
# This project uses a simpler JWT login approach,
# where the API itself authenticates the user and
# directly returns a JWT.
# ---------------------------------------------------------


async def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: AsyncSession = Depends(get_db)

):

    email = verify_token(token)

    if email is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return user


# =====================================================
# AUTH
# =====================================================

@app.post(
    "/api/v1/auth/register/",
    status_code=201
)
async def register(

    user: UserCreate,

    db: AsyncSession = Depends(get_db)

):

    existing = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    if existing.scalar_one_or_none():

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(

        email=user.email,

        hashed_password=get_password_hash(
            user.password
        )

    )

    db.add(new_user)

    await db.commit()

    return {

        "message": "User registered successfully"

    }


@app.post(
    "/api/v1/auth/login/",
    response_model=Token
)
async def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: AsyncSession = Depends(get_db)

):

    result = await db.execute(

        select(User).where(

            User.email == form_data.username

        )

    )

    user = result.scalar_one_or_none()

    if (
        user is None
        or
        not verify_password(
            form_data.password,
            user.hashed_password
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(

        data={
            "sub": user.email
        },

        expires_delta=timedelta(
            minutes=30
        )

    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }
# =====================================================
# COURSES
# =====================================================

@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="Returns the created course"
)
async def create_course(
    course: CourseCreate,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    new_course = Course(**course.model_dump())

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    response.headers["Location"] = f"/api/v1/courses/{new_course.id}"

    return new_course


@app.get(
    "/api/v1/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Course)

    if department_id is not None:
        query = query.where(
            Course.department_id == department_id
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


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
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
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
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    await db.delete(course)

    await db.commit()

    return Response(status_code=204)


@app.get(
    "/api/v1/courses/{course_id}/students/",
    tags=["Courses"]
)
async def get_course_students(course_id: int):

    return {
        "course_id": course_id,
        "students": [
            {
                "id": 1,
                "name": "Alice"
            },
            {
                "id": 2,
                "name": "Bob"
            }
        ]
    }


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
    tags=["Students"]
)
async def create_student(student: dict):

    students.append(student)

    return student


@app.put(
    "/api/v1/students/{student_id}",
    tags=["Students"]
)
async def update_student(student_id: int):

    return {
        "message": f"Student {student_id} updated"
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
    enrollment: dict,
    background_tasks: BackgroundTasks
):

    enrollments.append(enrollment)

    background_tasks.add_task(
        send_confirmation_email,
        enrollment["student_email"]
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


@app.delete(
    "/api/v1/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(enrollment_id: int):

    return Response(status_code=204)