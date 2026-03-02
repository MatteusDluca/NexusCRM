from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CardBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[float] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"
    tags: Optional[str] = None
    assignee_id: Optional[int] = None

class CardCreate(CardBase):
    title: str
    column_id: int
    order_index: float = 0.0

class CardUpdate(CardBase):
    column_id: Optional[int] = None # Permite arrastar o card pra outra coluna

class CardResponse(CardBase):
    id: int
    title: str
    description: Optional[str] = None
    column_id: int
    order_index: float
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"
    tags: Optional[str] = None
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True
