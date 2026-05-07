from pydantic import BaseModel
from typing import Optional, List
from app.schemas.task import TaskOut


class ProjectBase(BaseModel):
    """Base schema for Project containing common attributes."""
    name: str
    description: Optional[str] = None
    manager_id: int


class ProjectCreate(ProjectBase):
    """Schema for creating a new Project."""
    pass


class ProjectOut(ProjectBase):
    """Schema for standard Project responses (List view)."""
    id: int

    class Config:
        from_attributes = True


class ProjectDetailOut(ProjectOut):
    """Schema for detailed Project responses, including embedded tasks."""
    tasks: List[TaskOut] = []

    class Config:
        from_attributes = True