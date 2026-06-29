from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import user_repository
from app.core.security import get_password_hash
from app.core.exceptions import ResourceConflictException, ResourceNotFoundException

class UserService:
    def create_user(self, db: Session, *, user_in: UserCreate) -> User:
        """
        Create a new user.
        Validates that email is unique, hashes password, and saves to database.
        """
        # Check if email exists
        existing_user = user_repository.get_by_email(db, email=user_in.email)
        if existing_user:
            raise ResourceConflictException(f"Email {user_in.email} is already registered")
        
        # Hash password and create record
        user_data = user_in.model_dump()
        user_data["password_hash"] = get_password_hash(user_data.pop("password"))
        
        return user_repository.create(db, obj_in_data=user_data)

    def get_user_by_id(self, db: Session, *, user_id: UUID) -> User:
        """Retrieve user by UUID."""
        user = user_repository.get(db, id=user_id)
        if not user:
            raise ResourceNotFoundException("User")
        return user

    def list_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """List all users."""
        return user_repository.get_multi(db, skip=skip, limit=limit)

user_service = UserService()
