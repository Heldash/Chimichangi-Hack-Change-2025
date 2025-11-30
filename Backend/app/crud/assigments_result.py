from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.schemas import AssignmentResult


async def create_assignment_result(
    db: AsyncSession,
    assignment_id: int,
    teacher_comment: str | None,
    grade: int | None
):
    result = AssignmentResult(
        assignment_id=assignment_id,
        teacher_comment=teacher_comment,
        grade=grade
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


async def get_assignment_result(db: AsyncSession, assignment_id: int):
    result = await db.execute(
        select(AssignmentResult).where(AssignmentResult.assignment_id == assignment_id)
    )
    return result.scalar_one_or_none()


async def update_assignment_result(db: AsyncSession, assignment_id: int, **data):
    stmt = (
        update(AssignmentResult)
        .where(AssignmentResult.assignment_id == assignment_id)
        .values(**data)
        .returning(AssignmentResult)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_assignment_result(db: AsyncSession, assignment_id: int):
    await db.execute(
        delete(AssignmentResult).where(AssignmentResult.assignment_id == assignment_id)
    )
    await db.commit()
    return True
