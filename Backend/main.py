import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.initial_database import seed_database
from app.crud.users import get_user_by_username, create_user
from app.core.config import settings
from app.db.session import engine,AsyncSessionLocal
from app.db.base import Base
from app.api.auth import router as auth_router
from app.api.courses import router as courses_router
from app.api.materials import router as materials_router
from app.api.assignments import router as assignments_router
from app.api.user import router as user_router
from app.api.files import router as files_router
from app.api.health import router as health_router

app = FastAPI(title="Chimichangi backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/me", tags=["User"])
app.include_router(courses_router, prefix="/courses", tags=["Courses"])
app.include_router(materials_router, prefix="/materials", tags=["Materials"])
app.include_router(assignments_router, prefix="/assignments", tags=["Assignments"])
app.include_router(files_router, prefix="/files", tags=["Files"])
app.include_router(health_router, tags=["Health"])

@app.on_event("startup")
async def startup():
    # create tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # create default user if set in env
    default_user = settings.DEFAULT_ADMIN_USERNAME
    default_pass = settings.DEFAULT_ADMIN_PASSWORD
    async with AsyncSessionLocal() as db:
        await seed_database(db)
        if default_user and default_pass:
            existing = await get_user_by_username(db, default_user)
            if not existing:
                await create_user(db, default_user, default_pass, full_name="Admin")