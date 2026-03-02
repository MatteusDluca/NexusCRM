from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from models.user import User
from repositories.column import column_repo
from repositories.board import board_repo
from schemas.column import KanbanColumnCreate, KanbanColumnUpdate, KanbanColumnResponse

router = APIRouter()

@router.get("/board/{board_id}", response_model=List[KanbanColumnResponse])
def read_columns(
    board_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Busca as listas de um Kanban."""
    return column_repo.get_multi_by_board(db=db, board_id=board_id, skip=skip, limit=limit)

@router.post("/", response_model=KanbanColumnResponse)
def create_column(
    *,
    db: Session = Depends(get_db),
    column_in: KanbanColumnCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Cria uma nova Lista/Status dentro do Board (ex: WIP)"""
    # Validation
    board = board_repo.get(db, id=column_in.board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board associado não existe")
        
    return column_repo.create(db=db, obj_in=column_in)
