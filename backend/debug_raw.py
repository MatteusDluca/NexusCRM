import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from database.session import get_db
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models.base import Base
from models.user import User
from models.workspace import Workspace
from models.board import Board, KanbanColumn, Card

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

resp1 = client.post(
    "/api/v1/auth/register",
    json={"email": "login2@example.com", "name": "Login User", "password": "mypassword"}
)
print("REGISTER:", resp1.status_code, resp1.json())

resp2 = client.post(
    "/api/v1/auth/login",
    data={"username": "login2@example.com", "password": "mypassword"}
)
print("LOGIN:", resp2.status_code, resp2.json())
