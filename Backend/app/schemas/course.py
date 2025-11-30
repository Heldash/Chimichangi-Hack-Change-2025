from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..db import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Relations
    materials = relationship("Material", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")