from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum as SQLEnum
)

from sqlalchemy.orm import relationship

from datetime import datetime

import enum

from app.db.database import Base


class ProjectStatus(str, enum.Enum):
    """Enum representing the lifecycle state of a project."""

    PLANNING = "Planning"

    ACTIVE = "Active"

    ON_HOLD = "On Hold"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"


class ProjectPriority(str, enum.Enum):
    """Enum representing the business priority of a project."""

    LOW = "Low"

    MEDIUM = "Medium"

    HIGH = "High"

    CRITICAL = "Critical"


class Project(Base):
    """Database model representing a project entity."""

    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Core project information
    name = Column(
        String(100),
        index=True,
        nullable=False
    )

    description = Column(
        String(500)
    )

    # Project workflow status
    status = Column(
        SQLEnum(ProjectStatus),
        default=ProjectStatus.PLANNING
    )

    # Project priority level
    priority = Column(
        SQLEnum(ProjectPriority),
        default=ProjectPriority.MEDIUM
    )

    # Project deadline
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

    # Assigned Project Manager
    manager_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Relationships mapping
    manager = relationship(
        "User",
        back_populates="managed_projects"
    )

    # Cascade ensures tasks are deleted if the project is removed
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )