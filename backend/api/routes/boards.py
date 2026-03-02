from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from models.user import User
from repositories.board import board_repo
from repositories.workspace import workspace_repo
from schemas.board import BoardCreate, BoardUpdate, BoardResponse

router = APIRouter()

@router.get("/workspace/{workspace_id}", response_model=List[BoardResponse])
def read_boards(
    workspace_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    # Service validation (Security check: User should own Workspace to view Boards)
    workspace = workspace_repo.get(db, id=workspace_id)
    if not workspace or workspace.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace não encontrado ou você não tem permissão de leitura")
        
    boards = board_repo.get_multi_by_workspace(db=db, workspace_id=workspace_id, skip=skip, limit=limit)
    
    # Auto-healing (Se o Workspace foi criado antes do Patch do Default Board, crie ele agora)
    if not boards:
        from schemas.board import BoardCreate
        default_board = BoardCreate(name="Quadro Principal", workspace_id=workspace_id)
        board = board_repo.create(db=db, obj_in=default_board)
        boards = [board]
        
    return boards

@router.post("/", response_model=BoardResponse)
def create_board(
    *,
    db: Session = Depends(get_db),
    board_in: BoardCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    # Service validation (Security check: User should own Workspace to create Board)
    workspace = workspace_repo.get(db, id=board_in.workspace_id)
    if not workspace or workspace.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace inválido. Acesso não permitido para criar Quadros aqui.")
        
    board = board_repo.create(db=db, obj_in=board_in)
    return board
