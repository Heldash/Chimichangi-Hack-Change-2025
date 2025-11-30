from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,update
from app.schemas.user import User,MaterialView
from app.core.utils import hash_password


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_user(db: AsyncSession, username: str, password: str, full_name: str | None):
    user = User(
        username=username,
        hashed_password=hash_password(password),
        full_name=full_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, **data):
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**data)
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_user(db: AsyncSession, user_id: int):
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    return True

async def add_watched_material(db: AsyncSession, user_id: int,material_id:int,course_id:id):
    watched = MaterialView(material_id=material_id,
                           user_id=user_id,
                           course_id=course_id)
    db.add(watched)
    await db.commit()
    return True

async def get_watched_material_with_user(db: AsyncSession, user_id: int):
    stmt = select(MaterialView).where(MaterialView.user_id==user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

