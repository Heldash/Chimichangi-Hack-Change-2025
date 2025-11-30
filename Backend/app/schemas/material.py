from sqlalchemy import Column, Integer, String, Text, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class FilesWithMaterial(Base):
    __tablename__ = "files_materials"
    id = Column(Integer,primary_key=True,index=True)
    type = Column(String(20),nullable=False)
    object_name = Column(String(255), nullable=True)
    file_url = Column(String(500),nullable=False)
    material_id = Column(Integer,ForeignKey("materials.id"))
    material = relationship("Material",back_populates="pinned_files")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)  # text | video | file
    content_text = Column(Text, nullable=True)      # text content if any
    object_name = Column(String(255), nullable=True)  # minio s3 key
    file_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    have_assgiment = Column(Boolean, default=False)

    course_id = Column(Integer, ForeignKey("courses.id"))

    # Relations
    course = relationship("Course", back_populates="materials")
    assignments = relationship("Assignment", back_populates="material")
    pinned_files = relationship("FilesWithMaterial",back_populates="material")
