from pydantic import BaseModel
from typing import Optional
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
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None


class TaskOut(TaskBase):
    """
    Schema for Task responses returned by the API.
    Includes the database ID.
    """
    id: int

    class Config:
        from_attributes = True