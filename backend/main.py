from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.routes.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema Kanban Profissional, Assíncrono e Seguro. API para testes técnicos (Python/React)",
    version="1.0.0",
)

# CORS Policy - Necessário porque o React vai rodar numa porta e uvicorn na outra
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trocar por [http://localhost:3000] em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/healthz", tags=["healthz"])
async def health_check():
    """Endpoint vital recomendado em orquestradores (Kubernetes/Docker) para checar a saúde do contêiner."""
    return {"status": "ok", "app": "Nexus Board API is running"}
