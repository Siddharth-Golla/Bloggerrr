from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.auth import UserRegister


def register_user(db: Session, user_data: UserRegister) -> User:
    existing_user = db.scalar(
        select(User).where(
            (User.username == user_data.username)
            | (User.email == user_data.email)
        )
    )

    if existing_user:
        raise ValueError("Username or email already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user