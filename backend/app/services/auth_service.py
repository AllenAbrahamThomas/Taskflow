from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.core.exceptions import CredentialsException
from app.repositories.user_repository import user_repository
from app.schemas.user import Token

class AuthService:
    def authenticate_user(self, db: Session, *, email: str, password: str) -> Token:
        """
        Authenticate a user by email and password, returning a JWT token if successful.
        """
        user = user_repository.get_by_email(db, email=email)
        if not user or not verify_password(password, user.password_hash):
            raise CredentialsException()
        
        # Create access token with user ID subject
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer", user=user)

auth_service = AuthService()
