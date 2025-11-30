from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from app.schemas import Course,Material,Assignment



async def create_course(db: AsyncSession, title: str, description: str | None = None):
    c = Course(title=title, description=description)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c

async def get_course(db: AsyncSession, course_id: int):
    r = await db.execute(select(Course).where(Course.id == course_id))
    return r.scalar_one_or_none()

async def get_courses(db: AsyncSession):
    r = await db.execute(select(Course))
    return r.scalars().all()

async def update_course(db: AsyncSession, course_id: int, **data):
    stmt = update(Course).where(Course.id == course_id).values(**data).returning(Course)
    r = await db.execute(stmt)
    await db.commit()
    return r.scalar_one_or_none()

async def delete_course(db: AsyncSession, course_id: int):
    await db.execute(delete(Course).where(Course.id == course_id))
    await db.commit()
    return True

async def get_course_materials(db: AsyncSession, course_id: int):
    r = await db.execute(select(Material).where(Material.course_id == course_id))
    return r.scalars().all()

async def get_course_progress(db: AsyncSession, user_id: int, course_id: int):
    total = (await db.execute(select(func.count(Material.id)).where(Material.course_id == course_id))).scalar() or 0
    completed = (await db.execute(select(func.count(Assignment.id)).where(Assignment.course_id == course_id, Assignment.user_id == user_id))).scalar() or 0
    percent = round((completed / total) * 100, 2) if total else 0
    return {"completed_materials": completed, "total_materials": total, "percent": percent}
