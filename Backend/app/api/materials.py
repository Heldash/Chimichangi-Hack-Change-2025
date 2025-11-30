from fastapi import APIRouter, Depends, HTTPException,UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.core.minio_client import ensure_bucket, client
from app.schemas import User
from app.crud.materials import get_material,update_material
from app.crud.users import add_watched_material
from app.models import MaterialBase
import uuid
import io

router = APIRouter()
BUCKET_NAME = "materials"
@router.post("/{material_id}/upload")
async def upload_material_content( material_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    ensure_bucket(BUCKET_NAME)
    object_name = f"{material_id}/{uuid.uuid4().hex}_{file.filename}"
    data = await file.read()
    # upload to MinIO
    client.put_object(BUCKET_NAME, object_name, io.BytesIO(data), length=len(data), content_type=file.content_type)
    material = await update_material(db,material_id,object_name=object_name,file_url=f"/files/view/{object_name}")
    return {"material_id": material.id, "object_name": material.object_name,"file_url":material.file_url}
@router.get("/{material_id}", response_model=MaterialBase)
async def get_material_detail(material_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    material = await get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.post("/{material_id}/view")
async def mark_material_viewed(material_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    material = await get_material(db,material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    await add_watched_material(db,current_user.id,material.id,material.course_id)
    return {"status": "ok"}

