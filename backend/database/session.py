from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Engine configuration (Best Practice: pool_pre_ping checks if connection is alive)
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True, 
    pool_size=10, 
    max_overflow=20
)

# Fabrica de sessoes locais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency para ser usada nos controllers/routers do FastAPI.
    Garante que a sessão do DB seja conectada no inicio da Request e fechada no fim,
    mesmo que ocorra uma exceção de servidor (yield pattern).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
