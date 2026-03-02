from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.config import settings
from database.session import get_db
from models.user import User
from repositories.user import user_repo

# FastAPI lida com o token vindo no Header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Injeção de dependência crucial (DI). 
    Todas as rotas do Kanban que exigirem login colocarão isso como parâmetro.
    Valida assinatura do JWT, expiração e se o user ainda constar no banco ativo.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = user_repo.get(db, id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuário do Token não encontrado no Banco")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    return user
