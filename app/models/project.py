from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Project(Base):
    """Database model representing a project entity."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(500))
    manager_id = Column(Integer, ForeignKey("users.id"))

    # Relationships mapping
    manager = relationship("User", back_populates="managed_projects")

    # Cascade ensures tasks are deleted if the project is removed
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")