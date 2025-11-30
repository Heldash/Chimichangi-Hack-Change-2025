from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.schemas import Assignment


async def create_assignment(
    db: AsyncSession,
    user_id: int,
    course_id: int,
    material_id: int,
    file_name: str,
    object_name: str
):
    assignment = Assignment(
        user_id=user_id,
        course_id=course_id,
        material_id=material_id,
        file_name=file_name,
        object_name=object_name
    )
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment


async def get_assignment(db: AsyncSession, assignment_id: int):
    result = await db.execute(
        select(Assignment).where(Assignment.id == assignment_id)
    )
    return result.scalar_one_or_none()


async def get_assignments_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Assignment).where(Assignment.user_id == user_id)
    )
    return result.scalars().all()


async def update_assignment(db: AsyncSession, assignment_id: int, **data):
    stmt = (
        update(Assignment)
        .where(Assignment.id == assignment_id)
        .values(**data)
        .returning(Assignment)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_assignment(db: AsyncSession, assignment_id: int):
    await db.execute(delete(Assignment).where(Assignment.id == assignment_id))
    await db.commit()
    return True
