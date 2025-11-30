from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas import User
from app.crud.courses import get_courses, get_course, get_course_materials, get_course_progress
from app.models import CourseList
from app.models.material import MaterialList


router = APIRouter()

@router.get("/", response_model=list[CourseList])
async def list_courses(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_courses(db)

@router.get("/{course_id}", response_model=CourseList)
async def course_detail(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = await get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/{course_id}/materials", response_model=list[MaterialList])
async def course_materials(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_course_materials(db, course_id)

@router.get("/{course_id}/progress")
async def course_progress(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_course_progress(db, current_user.id, course_id)
