from typing import Optional, List
from pydantic import BaseModel

class BoardBase(BaseModel):
    name: Optional[str] = None

class BoardCreate(BoardBase):
    name: str
    workspace_id: int

class BoardUpdate(BoardBase):
    pass

class BoardResponse(BoardBase):
    id: int
    name: str
    workspace_id: int

    class Config:
        from_attributes = True
