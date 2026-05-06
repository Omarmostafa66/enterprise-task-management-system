from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.project import Project
from app.models.user import UserRole
from app.schemas.project import ProjectCreate, ProjectOut
from app.dependencies.auth import check_role, get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectOut)
def create_project(
        project_in: ProjectCreate,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    # Only Admin can create projects
    new_project = Project(**project_in.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[ProjectOut])
def list_projects(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    # All authenticated users can list projects
    return db.query(Project).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    # All authenticated users can view a specific project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
        project_id: int,
        project_in: ProjectCreate,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    # Only Admin can update projects
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update project attributes
    update_data = project_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(check_role([UserRole.ADMIN]))
):
    # Only Admin can delete projects
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}