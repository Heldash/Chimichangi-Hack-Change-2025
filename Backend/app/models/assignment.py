from pydantic import BaseModel

class AssignmentOut(BaseModel):
    id: int
    course_id: int
    material_id: int
    file_name: str

    class Config:
        from_attributes = True
