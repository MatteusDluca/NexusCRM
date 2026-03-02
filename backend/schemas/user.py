from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True

# Criado via API de Register
class UserCreate(UserBase):
    email: EmailStr
    name: str
    password: str

# Atualizado via API (tudo é opcional)
class UserUpdate(UserBase):
    password: Optional[str] = None

# Retornado no GET (Remove a senha)
class UserResponse(UserBase):
    id: int
    email: EmailStr
    name: str

    class Config:
        from_attributes = True

# Usado internamente no DB
class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True
