from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user