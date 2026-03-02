from typing import List
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime

from models.base import Base


class Board(Base):
    """
    O Board (Quadro do Kanban). Ele hospeda múltiplas Listas/Colunas.
    """
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    
    # Relacionamento M:1 com Workspace
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="boards")
    
    # Relacionamento 1:N com Colunas (Ex: To Do, Doing, Done)
    columns: Mapped[List["KanbanColumn"]] = relationship(
        "KanbanColumn", back_populates="board", cascade="all, delete-orphan", order_by="KanbanColumn.order_index"
    )


class KanbanColumn(Base):
    """
    As Colunas dentro do Board (ex: Para Fazer, Em Andamento).
    """
    __tablename__ = "columns"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    order_index: Mapped[float] = mapped_column(nullable=False, default=0.0) # Uso de float para facilitar reordenação sem reescrever BD
    
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    
    board: Mapped["Board"] = relationship("Board", back_populates="columns")
    
    cards: Mapped[List["Card"]] = relationship(
        "Card", back_populates="column", cascade="all, delete-orphan", order_by="Card.order_index"
    )


class Card(Base):
    """
    A Tarefa principal propriamente dita. O Container do UI que vai sofrer o Drag and Drop.
    """
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000))
    order_index: Mapped[float] = mapped_column(nullable=False, default=0.0)
    
    # Advanced Kanban Fields
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    priority: Mapped[str | None] = mapped_column(String(20), default="medium") # low, medium, high, urgent
    tags: Mapped[str | None] = mapped_column(String(200)) # Simple comma-separated tags for MVP
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    
    column: Mapped["KanbanColumn"] = relationship("KanbanColumn", back_populates="cards")
    assignee: Mapped["User"] = relationship("User")
