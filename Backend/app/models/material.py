from pydantic import BaseModel
from app.models.course import CourseList

class MaterialList(BaseModel):
    id: int
    title: str
    class Config:
        from_attributes = True
class FilesWithMaterial(BaseModel):
    id: int
    type: str
    file_url:str
    object_name:str
    material_id:int
    material:"MaterialGet"

class MaterialGet(MaterialList):
    file_url: str|None
    type: str
    content_text: str|None
    have_assigment:bool
    course: CourseList
    pinned_files: "FilesWithMaterial"