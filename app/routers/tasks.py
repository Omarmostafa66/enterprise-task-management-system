from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import UserRole
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.dependencies.auth import get_current_user, check_role
from app.utils.cache import (
    get_cached_data,
    set_cached_data,
    invalidate_cache
)
from app.services.task_service import validate_status_transition
from app.utils.logger import logger


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskOut])
def read_tasks(
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        assignee_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    Retrieve all tasks based on optional filters.
    Results are cached to improve performance.
    Authorization Rules: Employees can only view their own assigned tasks.
    """

    logger.info(
        f"Fetching tasks | "
        f"user={current_user.email} | "
        f"status={status} | "
        f"priority={priority} | "
        f"assignee_id={assignee_id}"
    )

    # Enforce Employee Authorization logic
    if current_user.role == UserRole.EMPLOYEE:
        assignee_id = current_user.id

    # Generate cache key using filters and current user
    cache_key = (
        f"tasks_all_"
        f"{current_user.id}_"
        f"{status}_"
        f"{priority}_"
        f"{assignee_id}"
    )

    # Attempt to retrieve cached tasks
    cached = get_cached_data(cache_key)

    if cached:
        logger.info(f"Returning tasks from cache | key={cache_key}")
        return cached

    # Build database query with optional filters
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)

    tasks = query.all()

    logger.info(
        f"Database query completed | "
        f"tasks_count={len(tasks)}"
    )

    # Convert tasks into serializable response format
    serialized_tasks = [
        TaskOut.from_orm(task).dict()
        for task in tasks
    ]

    # Cache query results for faster future access
    set_cached_data(cache_key, serialized_tasks)

    return tasks


@router.post("/", response_model=TaskOut)
def create_task(
        task_in: TaskCreate,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN, UserRole.PROJECT_MANAGER]))
):
    """
    Create a new task.
    Restricted to Admins and Project Managers.
    """

    logger.info(
        f"Creating new task | "
        f"title={task_in.title} | "
        f"user={current_user.email}"
    )

    new_task = Task(**task_in.dict())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(
        f"Task created successfully | "
        f"task_id={new_task.id}"
    )

    # Invalidate cache because the underlying data has changed
    invalidate_cache("tasks_")

    return new_task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
        task_id: int,
        task_in: TaskUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    Update an existing task by ID.
    Includes role-based restrictions and strict status transition validation.
    """

    logger.info(
        f"Updating task | "
        f"task_id={task_id} | "
        f"user={current_user.email}"
    )

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        logger.warning(f"Task not found | task_id={task_id}")

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Role validation: Employees can only update their explicitly assigned tasks
    if (
        current_user.role == UserRole.EMPLOYEE and
        task.assignee_id != current_user.id
    ):

        logger.warning(
            f"Unauthorized task update attempt | "
            f"user={current_user.email} | "
            f"task_id={task_id}"
        )

        raise HTTPException(
            status_code=403,
            detail="Employees can only update their assigned tasks"
        )

    # Status transition lifecycle validation
    if task_in.status and task_in.status != task.status:

        if not validate_status_transition(task.status, task_in.status):

            logger.warning(
                f"Invalid workflow transition | "
                f"task_id={task_id} | "
                f"from={task.status} | "
                f"to={task_in.status}"
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid workflow transition from "
                    f"{task.status} to {task_in.status}. "
                    f"Completed tasks cannot be modified."
                )
            )

    # Update only the provided fields from the payload
    update_data = task_in.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    logger.info(
        f"Task updated successfully | "
        f"task_id={task.id}"
    )

    # Invalidate cache because the underlying data has changed
    invalidate_cache("tasks_")

    return task


@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    """
    Delete a task by ID.
    Strictly restricted to Admin users.
    """

    logger.info(
        f"Deleting task | "
        f"task_id={task_id} | "
        f"user={current_user.email}"
    )

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:

        logger.warning(
            f"Delete failed - task not found | "
            f"task_id={task_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    logger.info(
        f"Task deleted successfully | "
        f"task_id={task_id}"
    )

    # Invalidate cache because the underlying data has changed
    invalidate_cache("tasks_")

    return {"message": "Task deleted successfully"}