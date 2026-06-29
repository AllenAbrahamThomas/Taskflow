from typing import Generator, List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import CredentialsException, PermissionDeniedException
from app.models.user import User
from app.repositories.user_repository import user_repository

# OAuth2PasswordBearer extracts the Bearer token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to authenticate request and return current user.
    Extracts JWT from Authorization header, decodes, and looks up User in DB.
    """
    payload = decode_access_token(token)
    if not payload:
        raise CredentialsException()
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise CredentialsException()
        
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise CredentialsException()
        
    user = user_repository.get(db, id=user_id)
    if not user:
        raise CredentialsException()
        
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        """
        Reusable dependency class to enforce Role-Based Access Control.
        """
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise PermissionDeniedException(
                detail=f"Access denied. Required role: one of {self.allowed_roles}"
            )
        return current_user

# Predefined role helpers
require_admin = RoleChecker(["admin"])
require_developer = RoleChecker(["developer"])
require_any_role = RoleChecker(["admin", "developer"])
