from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.database import Base


class TaskStatus(str, enum.Enum):
    """Enum representing the current status of a task."""
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class TaskPriority(str, enum.Enum):
    """Enum representing the priority level of a task."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Task(Base):
    """Database model for tasks."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    # Core task information
    title = Column(
        String(200),
        index=True,
        nullable=False
    )  # Length of 200 characters

    description = Column(
        String(1000)
    )  # Length of 1000 characters for detailed description

    # Task workflow fields
    status = Column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO
    )

    priority = Column(
        SQLEnum(TaskPriority),
        default=TaskPriority.MEDIUM
    )

    # Task deadline support
    due_date = Column(
        DateTime,
        nullable=True
    )

    # Automatic timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Foreign Keys
    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    assignee_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Relationships
    project = relationship(
        "Project",
        back_populates="tasks"
    )

    assignee = relationship(
        "User",
        back_populates="assigned_tasks"
    )