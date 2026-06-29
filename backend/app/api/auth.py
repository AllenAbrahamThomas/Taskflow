from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db
from app.services.auth_service import auth_service
from app.schemas.user import Token

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=Token)
def login(request_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Log in a user.
    Receives email and password, validates, and returns a bearer access token.
    """
    return auth_service.authenticate_user(
        db, 
        email=request_data.email, 
        password=request_data.password
    )
