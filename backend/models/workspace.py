from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from models.base import Base


class Workspace(Base):
    """
    Agrupador principal. Um Workspace (Ex: "Projeto Alpha") contém vários Boards.
    """
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(300))
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relação com Usuário proprietário
    owner: Mapped["User"] = relationship("User", back_populates="workspaces")
    
    # Relação 1:N com Boards
    boards: Mapped[List["Board"]] = relationship(
        "Board", back_populates="workspace", cascade="all, delete-orphan"
    )
