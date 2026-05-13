from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.project import Project
from app.models.user import UserRole
from app.schemas.project import (
    ProjectCreate,
    ProjectOut,
    ProjectDetailOut
)
from app.dependencies.auth import (
    check_role,
    get_current_user
)
from app.utils.logger import logger


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectOut)
def create_project(
        project_in: ProjectCreate,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    """
    Create a new project.
    Strictly restricted to Admin users.
    """

    logger.info(
        f"Creating project | "
        f"name={project_in.name} | "
        f"user={current_user.email}"
    )

    # Validate project due date
    if (
        project_in.due_date and
        project_in.due_date < datetime.utcnow()
    ):

        logger.warning(
            f"Invalid project due date | "
            f"name={project_in.name}"
        )

        raise HTTPException(
            status_code=400,
            detail="Project due date cannot be in the past"
        )

    new_project = Project(**project_in.dict())

    db.add(new_project)

    db.commit()

    db.refresh(new_project)

    logger.info(
        f"Project created successfully | "
        f"project_id={new_project.id}"
    )

    return new_project


@router.get("/", response_model=list[ProjectOut])
def list_projects(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    Retrieve a list of all projects.
    Available to all authenticated users.
    """

    logger.info(
        f"Fetching all projects | "
        f"user={current_user.email}"
    )

    projects = db.query(Project).all()

    logger.info(
        f"Projects retrieved successfully | "
        f"count={len(projects)}"
    )

    return projects


@router.get("/{project_id}", response_model=ProjectDetailOut)
def get_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    Retrieve specific project details,
    including an array of its tasks.
    Used for the detailed project modal view.
    """

    logger.info(
        f"Fetching project details | "
        f"project_id={project_id} | "
        f"user={current_user.email}"
    )

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:

        logger.warning(
            f"Project not found | "
            f"project_id={project_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
        project_id: int,
        project_in: ProjectCreate,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    """
    Update project attributes.
    Restricted to Admin users.
    """

    logger.info(
        f"Updating project | "
        f"project_id={project_id} | "
        f"user={current_user.email}"
    )

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:

        logger.warning(
            f"Project update failed - not found | "
            f"project_id={project_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # Validate due date update
    if (
        project_in.due_date and
        project_in.due_date < datetime.utcnow()
    ):

        logger.warning(
            f"Invalid due date update | "
            f"project_id={project_id}"
        )

        raise HTTPException(
            status_code=400,
            detail="Project due date cannot be in the past"
        )

    update_data = project_in.dict(exclude_unset=True)

    for key, value in update_data.items():

        setattr(project, key, value)

    db.commit()

    db.refresh(project)

    logger.info(
        f"Project updated successfully | "
        f"project_id={project.id}"
    )

    return project


@router.delete("/{project_id}")
def delete_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    """
    Delete a project entirely from the system.
    Strictly restricted to Admin users.
    """

    logger.info(
        f"Deleting project | "
        f"project_id={project_id} | "
        f"user={current_user.email}"
    )

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:

        logger.warning(
            f"Project delete failed - not found | "
            f"project_id={project_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)

    db.commit()

    logger.info(
        f"Project deleted successfully | "
        f"project_id={project_id}"
    )

    return {
        "message": "Project deleted successfully"
    }