from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.user import User
from app.schemas.course import Course
from app.schemas.material import Material
from app.core.utils import hash_password


async def seed_database(db: AsyncSession):

    # ---- Check if already seeded ----
    users = await db.execute(select(User))
    if users.scalars().first():
        print("[SEED] Database already seeded")
        return

    print("[SEED] Seeding database...")

    # ---- Users ----
    user1 = User(
        username="student1",
        hashed_password=hash_password("123456"),
        full_name="Иван Петров"
    )

    user2 = User(
        username="student2",
        hashed_password=hash_password("123456"),
        full_name="Мария Смирнова"
    )

    teacher = User(
        username="teacher1",
        hashed_password=hash_password("teacherpass"),
        full_name="Преподаватель ПСБ"
    )

    db.add_all([user1, user2, teacher])
    await db.flush()

    # ---- Courses ----
    course1 = Course(
        title="Python для начинающих",
        description="Курс по основам Python"
    )
    course2 = Course(
        title="FastAPI интенсив",
        description="Построение backend на FastAPI"
    )

    db.add_all([course1, course2])
    await db.flush()

    # ---- Materials ----
    mat1 = Material(
        title="Введение в Python",
        type="text",
        content="Python — популярный язык программирования...",
        course_id=course1.id
    )

    mat2 = Material(
        title="Переменные и типы данных",
        type="video",
        video_url="https://example.com/video1.mp4",
        course_id=course1.id
    )

    mat3 = Material(
        title="Установка FastAPI",
        type="text",
        content="FastAPI — высокопроизводительный веб-фреймворк...",
        course_id=course2.id
    )

    db.add_all([mat1, mat2, mat3])
    await db.commit()

    print("[SEED] Done.")