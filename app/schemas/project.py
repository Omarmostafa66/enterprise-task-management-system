from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.schemas.task import TaskOut
from app.models.project import (
    ProjectStatus,
    ProjectPriority
)


class ProjectBase(BaseModel):
    """Base schema for Project containing common attributes."""

    # Core project information
    name: str

    description: Optional[str] = None

    manager_id: int

    # Project workflow status
    status: ProjectStatus = ProjectStatus.PLANNING

    # Project business priority
    priority: ProjectPriority = ProjectPriority.MEDIUM

    # Optional project deadline
    due_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new Project."""

    pass


class ProjectOut(ProjectBase):
    """Schema for standard Project responses (List view)."""

    id: int

    # Audit timestamps
    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectDetailOut(ProjectOut):
    """
    Schema for detailed Project responses,
    including embedded tasks.
    """

    tasks: List[TaskOut] = []

    class Config:
        from_attributes = True