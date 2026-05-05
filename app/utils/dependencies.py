from typing import Optional

from fastapi import Depends, Header, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel


api_key_header = APIKeyHeader(name="x-user-role", auto_error=False)


class UserContext(BaseModel):
    user_id: Optional[str] = None
    role: str = "user"


def get_user_context(
    x_user_role: Optional[str] = Security(api_key_header),
    x_user_id: Optional[str] = Header(None),
) -> UserContext:
    role = x_user_role or "user"
    return UserContext(user_id=x_user_id, role=role)


def require_admin(user: UserContext = Depends(get_user_context)) -> UserContext:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
