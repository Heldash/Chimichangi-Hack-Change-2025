from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)

    # Relations
    assignments = relationship("Assignment", back_populates="user")
    material_view = relationship("MaterialView",back_populates="user")


class MaterialView(Base):
    __tablename__ = "material_view"
    id = Column(Integer,primary_key=True,index=True)
    material_id = Column(Integer,ForeignKey("materials.id"))
    user_id = Column(Integer,ForeignKey("users.id"))
    course_id = Column(Integer,ForeignKey("courses.id"))

    # Relations
    user = relationship("User",back_populates="material_view")

