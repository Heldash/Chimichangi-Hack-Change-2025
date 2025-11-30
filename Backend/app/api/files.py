from fastapi import APIRouter, UploadFile, File, Path,HTTPException
from fastapi.responses import StreamingResponse
from app.core.minio_client import client
import io

router = APIRouter()

@router.get("/files/view/{object_name}")
async def view_file(object_name: str):
    try:
        data = client.get_object("assignments", object_name)
        content = data.read()

        # определяем тип
        if object_name.lower().endswith((".jpg", ".jpeg", ".png")):
            media = "image/jpeg" if object_name.endswith("jpg") else "image/png"
        elif object_name.lower().endswith((".mp4", ".webm", ".ogg")):
            media = "video/mp4"
        else:
            media = "application/octet-stream"

        return StreamingResponse(io.BytesIO(content), media_type=media)

    except Exception as e:
        raise HTTPException(404, "File not found")
