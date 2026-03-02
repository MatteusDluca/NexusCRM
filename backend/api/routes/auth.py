from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_access_token
from database.session import get_db
from repositories.user import user_repo
from schemas.user import UserResponse, UserCreate
from services.user_service import UserService
from api.dependencies import get_current_user
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, requisita email como 'username' e a 'password' em form-data.
    """
    user = user_repo.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserResponse)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Cria nova conta validando duplicidade. Password será automaticamente Encrypted no repo.
    """
    try:
        user = UserService.register_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: UserResponse = Depends(get_current_user)
) -> Any:
    """
    Endpoint Rápido (Profile) para o Frontend ver se o token gravado nos Cookies/Local Storage é válido.
    """
    return current_user
