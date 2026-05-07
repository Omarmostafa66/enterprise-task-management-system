from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class UserRole(str, enum.Enum):
    """Enum representing the access roles for users."""
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    EMPLOYEE = "employee"


class User(Base):
    """Database model for users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)

    # Soft delete flag to maintain database integrity (Foreign Keys)
    is_active = Column(Boolean, default=True)

    # Relationships
    managed_projects = relationship("Project", back_populates="manager")
    assigned_tasks = relationship("Task", back_populates="assignee")