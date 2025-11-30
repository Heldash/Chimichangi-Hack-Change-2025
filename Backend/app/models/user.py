from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    username: str
    full_name: str | None

    class Config:
        from_attributes = True
