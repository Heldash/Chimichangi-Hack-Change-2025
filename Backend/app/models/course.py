from pydantic import BaseModel

class CourseList(BaseModel):
    id: int
    title: str
    description: str | None

    class Config:
        from_attributes = True
