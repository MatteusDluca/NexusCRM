from typing import List
from sqlalchemy.orm import Session
from models.board import Board
from schemas.board import BoardCreate, BoardUpdate
from repositories.base import RepositoryBase

class RepositoryBoard(RepositoryBase[Board, BoardCreate, BoardUpdate]):
    def get_multi_by_workspace(self, db: Session, *, workspace_id: int, skip: int = 0, limit: int = 100) -> List[Board]:
        return db.query(self.model).filter(Board.workspace_id == workspace_id).offset(skip).limit(limit).all()

board_repo = RepositoryBoard(Board)
