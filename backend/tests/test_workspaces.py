from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def get_auth_token(client: TestClient) -> str:
    """Helper genérico para injetar no client do pytest e logar o usuário antes do teste rolar"""
    client.post(
        "/api/v1/auth/register",
        json={"email": "kanban@example.com", "name": "Kanban Master", "password": "pwd"}
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "kanban@example.com", "password": "pwd"}
    )
    return login_resp.json()["access_token"]

def test_create_workspace(client: TestClient, db: Session):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Post protegido
    response = client.post(
        "/api/v1/workspaces/",
        headers=headers,
        json={"name": "Projeto Alpha", "description": "Lançamento em 2024"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Projeto Alpha"
    assert "id" in data
    
    # Garantia de Ownership: o ID do dono deve ser 1 (Primeiro User criado no SQLite da function)
    assert data["owner_id"] == 1 

def test_create_workspace_unauthorized(client: TestClient):
    # Sem Header
    response = client.post(
        "/api/v1/workspaces/",
        json={"name": "Inválido"}
    )
    assert response.status_code == 401
