from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    login: str = "postgres"
    password:str = "postgres"
    port:int = 5432
    host:str = "0.0.0.0"
    database:str = "hackathon_db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin"
    MINIO_ENDPOINT:str = "minio:9000"
    MINIO_ACCESS_KEY:str = "admin"
    MINIO_SECRET_KEY:str = "admin12345"
    MINIO_SECURE:bool = False

    @property
    def DATABASE_URL(self):
        # return "postgresql+asyncpg://postgres:Hakaton2025@95.165.80.92:5432/posgress"
        return f"postgresql+asyncpg://{self.login}:{self.password}@db:5433/{self.db}"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()