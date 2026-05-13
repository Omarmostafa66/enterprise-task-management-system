from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """
    Base schema for Task containing common attributes.
    """

    title: str

    description: Optional[str] = None

    status: TaskStatus = TaskStatus.TODO

    priority: TaskPriority = TaskPriority.MEDIUM

    project_id: int

    assignee_id: Optional[int] = None

    # Task deadline support
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """
    Schema for creating a new Task.
    Inherits all attributes from TaskBase.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing Task.
    All fields are optional to allow partial updates.
    """

    title: Optional[str] = None

    description: Optional[str] = None

    status: Optional[TaskStatus] = None

    priority: Optional[TaskPriority] = None

    assignee_id: Optional[int] = None

    # Allow updating task deadlines
    due_date: Optional[datetime] = None


class TaskOut(TaskBase):
    """
    Schema for Task responses returned by the API.
    Includes the database ID and timestamps.
    """

    id: int

    # Audit timestamps
    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True