from minio import Minio
from app.core.config import settings


MINIO_ENDPOINT =settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY =settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY =settings.MINIO_SECRET_KEY
MINIO_SECURE =settings.MINIO_SECURE

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)


def ensure_bucket(bucket_name: str):
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
    except Exception:
        # best-effort: ignore errors here (e.g. when MinIO not ready during startup)
        pass
