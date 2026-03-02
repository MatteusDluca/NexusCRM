from typing import Optional
from pydantic import BaseModel

class KanbanColumnBase(BaseModel):
    name: Optional[str] = None
    order_index: Optional[float] = None

class KanbanColumnCreate(KanbanColumnBase):
    name: str
    board_id: int
    order_index: float = 0.0

class KanbanColumnUpdate(KanbanColumnBase):
    pass

class KanbanColumnResponse(KanbanColumnBase):
    id: int
    name: str
    board_id: int
    order_index: float

    class Config:
        from_attributes = True
