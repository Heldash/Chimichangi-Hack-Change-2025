# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.core.utils import verify_password
from app.crud.users import create_user, get_user_by_username
from pydantic import BaseModel

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    password: str
    full_name: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = await create_user(
        db,
        username=payload.username,
        password=payload.password,
        full_name=payload.full_name
    )
    return {"id": user.id, "username": user.username}


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(access_token=access_token)
