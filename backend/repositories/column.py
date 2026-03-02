from typing import List
from sqlalchemy.orm import Session
from models.board import KanbanColumn
from schemas.column import KanbanColumnCreate, KanbanColumnUpdate
from repositories.base import RepositoryBase

class RepositoryColumn(RepositoryBase[KanbanColumn, KanbanColumnCreate, KanbanColumnUpdate]):
    def get_multi_by_board(self, db: Session, *, board_id: int, skip: int = 0, limit: int = 100) -> List[KanbanColumn]:
        return db.query(self.model).filter(KanbanColumn.board_id == board_id).order_by(KanbanColumn.order_index).offset(skip).limit(limit).all()

column_repo = RepositoryColumn(KanbanColumn)
