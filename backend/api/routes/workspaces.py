from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from models.user import User
from repositories.workspace import workspace_repo
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse

# Todas as rotas deste router EXIGEM usuário logado (token JWT válido)
router = APIRouter()


@router.get("/", response_model=List[WorkspaceResponse])
def read_workspaces(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Lista APENAS os Workspaces em que o usuário logado é Owner.
    """
    workspaces = workspace_repo.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return workspaces


from repositories.board import board_repo
from schemas.board import BoardCreate

@router.post("/", response_model=WorkspaceResponse)
def create_workspace(
    *,
    db: Session = Depends(get_db),
    workspace_in: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Cria um Workspace designando o usuário logado como Owner e gera um Quadro Padrão inicial.
    """
    workspace = workspace_repo.create_with_owner(db=db, obj_in=workspace_in, owner_id=current_user.id)
    
    # Cria automaticamente um Default Board
    default_board = BoardCreate(name="Quadro Principal", workspace_id=workspace.id)
    board_repo.create(db=db, obj_in=default_board)
    
    return workspace
