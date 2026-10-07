from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.core.security import create_access_token,hash_password,verify_password
from app.schemas.auth import UserLogin, UserRegister

def register_user(db: Session, user_data: UserRegister) -> User:
    existing_user = db.scalar(
        select(User).where(
            (User.username == user_data.username)
            | (User.email == user_data.email)
        )
    )

    if existing_user:
        raise ValueError("Username or email already exists")

    member_role = db.scalar(
        select(Role).where(Role.name == "Member")
    )

    if member_role is None:
        raise ValueError("Default Member role is not configured")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role_id=member_role.id,
        is_active=True,
        is_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(db: Session, user_data: UserLogin) -> str:
    user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if not user or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("Invalid email or password")

    return create_access_token(user.id)