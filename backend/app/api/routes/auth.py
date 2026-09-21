from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserRegister, UserResponse
from app.services.auth import register_user
from app.schemas.auth import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth import login_user, register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

from app.api.dependencies import get_current_user
from app.models.user import User


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        return register_user(db, user_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        access_token = login_user(db, user_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user