from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import UserRole
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.dependencies.auth import get_current_user, check_role
from app.utils.cache import get_cached_data, set_cached_data, invalidate_cache
from app.services.task_service import validate_status_transition

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskOut])
def read_tasks(
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        assignee_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    # 1. Attempt to fetch data from cache with filters included in the key
    cache_key = f"tasks_all_{current_user.id}_{status}_{priority}_{assignee_id}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    # 2. If not in cache, fetch from DB and apply filters
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)

    tasks = query.all()

    # 3. Save to cache before returning
    set_cached_data(cache_key, [TaskOut.from_orm(t).dict() for t in tasks])
    return tasks


@router.post("/", response_model=TaskOut)
def create_task(
        task_in: TaskCreate,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN, UserRole.PROJECT_MANAGER]))
):
    new_task = Task(**task_in.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Invalidate cache because data has changed
    invalidate_cache("tasks_")
    return new_task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
        task_id: int,
        task_in: TaskUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Role validation: Employees can only update their assigned tasks
    if current_user.role == UserRole.EMPLOYEE and task.assignee_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Employees can only update their assigned tasks"
        )

    # Status transition lifecycle validation
    if task_in.status and task_in.status != task.status:
        if not validate_status_transition(task.status, task_in.status):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from {task.status} to {task_in.status}"
            )

    # Update only provided data
    update_data = task_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    # Invalidate cache because data has changed
    invalidate_cache("tasks_")
    return task


@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))  # Only Admin can delete
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    # Invalidate cache because data has changed
    invalidate_cache("tasks_")
    return {"message": "Task deleted successfully"}