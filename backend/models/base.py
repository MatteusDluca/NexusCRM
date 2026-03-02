from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy Models (SQL Tables).
    Will be used by Alembic to auto-generate database migrations.
    """
    pass
