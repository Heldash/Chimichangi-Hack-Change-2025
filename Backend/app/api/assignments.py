from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.core.minio_client import ensure_bucket, client
from app.crud.assigments import create_assignment, get_assignment
from app.crud.assigments_result import get_assignment_result
from app.schemas import User
import uuid
import io

router = APIRouter()
BUCKET = "assignments"

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_assignment(course_id: int = Form(...), material_id: int = Form(...), file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    ensure_bucket(BUCKET)
    object_name = f"{current_user.id}/{uuid.uuid4().hex}_{file.filename}"
    data = await file.read()
    # upload to MinIO
    client.put_object(BUCKET, object_name, io.BytesIO(data), length=len(data), content_type=file.content_type)
    assignment = await create_assignment(db, current_user.id, course_id, material_id, file.filename, object_name)
    return {"assignment_id": assignment.id, "object_name": assignment.object_name}

@router.get("/{assignment_id}")
async def get_assignment_route(assignment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    a = await get_assignment(db, assignment_id)
    if not a or a.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return a

@router.get("/{assignment_id}/result")
async def get_result(assignment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    a = await get_assignment(db, assignment_id)
    if not a or a.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Assignment not found")
    res = await get_assignment_result(db, assignment_id)
    return res or {"assignment_id": assignment_id, "teacher_comment": None, "grade": None}
