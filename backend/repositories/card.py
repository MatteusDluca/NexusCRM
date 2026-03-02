from typing import List
from sqlalchemy.orm import Session
from models.board import Card
from schemas.card import CardCreate, CardUpdate
from repositories.base import RepositoryBase

class RepositoryCard(RepositoryBase[Card, CardCreate, CardUpdate]):
    def get_multi_by_column(self, db: Session, *, column_id: int, skip: int = 0, limit: int = 100) -> List[Card]:
        return db.query(self.model).filter(Card.column_id == column_id).order_by(Card.order_index).offset(skip).limit(limit).all()

card_repo = RepositoryCard(Card)
