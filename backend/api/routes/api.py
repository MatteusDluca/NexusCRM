from fastapi import APIRouter
from api.routes import auth, workspaces, boards, columns, cards, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(boards.router, prefix="/boards", tags=["boards"])
api_router.include_router(columns.router, prefix="/columns", tags=["columns"])
api_router.include_router(cards.router, prefix="/cards", tags=["cards"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
