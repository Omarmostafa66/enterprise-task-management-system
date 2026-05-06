from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False) # طول 100 حرف
    description = Column(String(500)) # طول 500 حرف للوصف
    manager_id = Column(Integer, ForeignKey("users.id"))

    # العلاقات
    manager = relationship("User", back_populates="managed_projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")