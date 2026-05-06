from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False) # طول 100 حرف
    email = Column(String(150), unique=True, index=True, nullable=False) # طول 150 حرف
    hashed_password = Column(String(255), nullable=False) # الباسورد المشفر يحتاج مساحة أكبر
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)

    # العلاقات
    managed_projects = relationship("Project", back_populates="manager")
    assigned_tasks = relationship("Task", back_populates="assignee")