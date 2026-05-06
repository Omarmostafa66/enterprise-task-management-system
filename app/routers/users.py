from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserOut
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    db_user = (
        db.query(User)
        .filter(User.email == user_in.email)
        .first()
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    # Validate credentials
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    # Generate JWT token
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    # Return token + role
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": str(user.role)
    }