from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from models.user import User
from schemas.user import UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Busca usuários do sistema para designação/atribuição."""
    # Para o MVP nós listamos todos os usuários ativos
    users = db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    return users
