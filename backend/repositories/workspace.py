from sqlalchemy.orm import Session
from models.workspace import Workspace
from schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from repositories.base import RepositoryBase
from typing import List

class RepositoryWorkspace(RepositoryBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: WorkspaceCreate, owner_id: int) -> Workspace:
        obj_in_data = obj_in.model_dump()
        # Injeta o owner diretamente na instância do SQLAlchemy ignorando o Schema Pydantic
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Workspace]:
        return db.query(self.model).filter(Workspace.owner_id == owner_id).offset(skip).limit(limit).all()

workspace_repo = RepositoryWorkspace(Workspace)
