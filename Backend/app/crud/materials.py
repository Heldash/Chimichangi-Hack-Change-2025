from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.schemas import Material


async def create_material(
    db: AsyncSession,
    title: str,
    type: str,
    course_id: int,
    content: str | None = None,
    file_url: str | None = None,
    video_url: str | None = None
):
    material = Material(
        title=title,
        type=type,
        course_id=course_id,
        content=content,
        file_url=file_url,
        video_url=video_url,
    )
    db.add(material)
    await db.commit()
    await db.refresh(material)
    return material


async def get_material(db: AsyncSession, material_id: int) ->Material:
    result = await db.execute(select(Material).where(Material.id == material_id))
    return result.scalar_one_or_none()


async def get_materials(db: AsyncSession):
    result = await db.execute(select(Material))
    return result.scalars().all()


async def get_materials_by_course(db: AsyncSession, course_id: int):
    result = await db.execute(select(Material).where(Material.course_id == course_id))
    return result.scalars().all()


async def update_material(db: AsyncSession, material_id: int, **data):
    stmt = (
        update(Material)
        .where(Material.id == material_id)
        .values(**data)
        .returning(Material)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_material(db: AsyncSession, material_id: int):
    await db.execute(delete(Material).where(Material.id == material_id))
    await db.commit()
    return True

