from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from ..db import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    object_name = Column(String(255), nullable=False)  # minio s3 key
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # FK
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))

    # Relations
    user = relationship("User", back_populates="assignments")
    course = relationship("Course", back_populates="assignments")
    material = relationship("Material", back_populates="assignments")
    result = relationship("AssignmentResult", back_populates="assignment", uselist=False)


class AssignmentResult(Base):
    __tablename__ = "assignment_results"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), unique=True)

    teacher_comment = Column(Text, nullable=True)
    grade = Column(Integer, nullable=True)

    # Relations
    assignment = relationship("Assignment", back_populates="result")