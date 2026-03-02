from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from repositories.user import user_repo

def test_register_user_success(client: TestClient, db: Session):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "name": "John Doe", "password": "securepassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data # Segurança: Senha não deve vazar no JSON

def test_register_duplicate_email(client: TestClient, db: Session):
    # Setup inicial
    user_in = UserCreate(email="duplicate@example.com", name="Jane", password="pwd")
    user_repo.create(db, obj_in=user_in)
    
    # Tenta registrar o mesmo email na API
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "name": "Jane 2", "password": "newpwd"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "O email duplicate@example.com já está em uso."

def test_login_success_returns_jwt(client: TestClient, db: Session):
    # Cria user
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "name": "Login User", "password": "mypassword"}
    )
    
    # Tenta logar via OAuth2 Form Data
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "mypassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_me_with_valid_token(client: TestClient, db: Session):
    client.post(
        "/api/v1/auth/register",
        json={"email": "me@example.com", "name": "Me User", "password": "pwd"}
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "me@example.com", "password": "pwd"}
    )
    token = login_resp.json()["access_token"]
    
    # Chama rota protegida com o header
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"

def test_read_me_without_token_fails(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401 # Unauthorized
