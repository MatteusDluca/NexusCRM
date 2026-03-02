from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from repositories.user import user_repo

class UserService:
    """
    Business Logic Layer. Isola regras de negócio complexas.
    O Controller vai apenas repassar o JSON Pydantic para este serviço.
    """
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> User:
        user_exists = user_repo.get_by_email(db, email=user_in.email)
        if user_exists:
            # Em um app Real usaríamos Exception customizada pro FastAPI pegar, mas usaremos ValueError nativo por hora
            raise ValueError(f"O email {user_in.email} já está em uso.")
            
        return user_repo.create(db, obj_in=user_in)
