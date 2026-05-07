from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)
from app.dependencies.auth import check_role
from app.utils.logger import get_recent_logs

router = APIRouter(
    prefix="/auth",
    tags=["Authentication and Users"]
)


class UserRoleUpdate(BaseModel):
    """Schema for updating a user's role."""
    role: UserRole


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user in the system."""
    db_user = db.query(User).filter(User.email == user_in.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT access token."""
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not getattr(user, "is_active", True):
        raise HTTPException(status_code=403, detail="Account is deactivated")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": str(user.role)
    }


# ==========================================
# USER MANAGEMENT ENDPOINTS FOR ADMINS
# ==========================================

@router.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db),
                  current_user=Depends(check_role([UserRole.ADMIN, UserRole.PROJECT_MANAGER]))):
    """Retrieve all users. Restricted to Admin and Project Managers."""
    return db.query(User).all()


@router.put("/users/{user_id}/role", response_model=UserOut)
def update_user_role(user_id: int, role_update: UserRoleUpdate, db: Session = Depends(get_db),
                     current_user=Depends(check_role([UserRole.ADMIN]))):
    """Update a user's role. Strictly restricted to Admin users."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def deactivate_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(check_role([UserRole.ADMIN]))):
    """Soft delete: Deactivate a user to preserve foreign key constraints."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}


@router.put("/users/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(check_role([UserRole.ADMIN]))):
    """Reactivate a previously disabled user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()
    return {"message": "User activated successfully"}


@router.get("/users/{user_id}/details")
def get_user_details(user_id: int, db: Session = Depends(get_db),
                     current_user=Depends(check_role([UserRole.ADMIN, UserRole.PROJECT_MANAGER]))):
    """Fetch complete details of a specific user including assigned tasks and projects."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": getattr(user, "is_active", True),
        "managed_projects": [{"id": p.id, "name": p.name} for p in
                             user.managed_projects] if user.managed_projects else [],
        "assigned_tasks": [{"id": t.id, "title": t.title, "status": t.status} for t in
                           user.assigned_tasks] if user.assigned_tasks else []
    }


@router.get("/audit-logs")
def read_audit_logs(current_user=Depends(check_role([UserRole.ADMIN]))):
    """Retrieve system audit logs. Restricted to Admin users."""
    logs = get_recent_logs(100)
    return {"logs": logs}