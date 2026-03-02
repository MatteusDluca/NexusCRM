from typing import Optional
from pydantic import BaseModel
from schemas.user import UserResponse

class WorkspaceBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class WorkspaceCreate(WorkspaceBase):
    name: str

class WorkspaceUpdate(WorkspaceBase):
    pass

class WorkspaceResponse(WorkspaceBase):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True
