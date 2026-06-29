from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Create a new user.
    Admin role required. Checks for email conflicts and hashes password automatically.
    """
    return user_service.create_user(db, user_in=user_in)

@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    List users.
    Any logged-in user can access this to fetch users for task assignments.
    """
    return user_service.list_users(db, skip=skip, limit=limit)
