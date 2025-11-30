from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models import UserBase
from app.schemas import User

router = APIRouter()

@router.get("/", response_model=UserBase)
async def me(current_user: User = Depends(get_current_user)):
    return current_user

