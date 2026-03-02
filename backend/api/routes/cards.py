from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from models.user import User
from repositories.card import card_repo
from schemas.card import CardCreate, CardUpdate, CardResponse

router = APIRouter()

@router.get("/column/{column_id}", response_model=List[CardResponse])
def read_cards(
    column_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    return card_repo.get_multi_by_column(db=db, column_id=column_id, skip=skip, limit=limit)

@router.post("/", response_model=CardResponse)
def create_card(
    *,
    db: Session = Depends(get_db),
    card_in: CardCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    return card_repo.create(db=db, obj_in=card_in)

@router.put("/{card_id}", response_model=CardResponse)
def update_card(
    *,
    db: Session = Depends(get_db),
    card_id: int,
    card_in: CardUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Endpoint essencial para o Drag and Drop (mudança de ID de coluna)"""
    card = card_repo.get(db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card não encontrado")
    
    # Chama o generic update instanciando o model antigo e sobrescrevendo as propriedades da nova requisição (Pydantic)
    card = card_repo.update(db=db, db_obj=card, obj_in=card_in)
    return card
