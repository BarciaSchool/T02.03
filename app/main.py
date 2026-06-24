from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import categoria as categoria_controller
from app.core.config import settings
from app.core.database import Base, engine
from app.models.categoria import Categoria  # noqa: F401  (registra la tabla en metadata)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas al iniciar (para producción real usar Alembic)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "API REST para la gestión de **Categorías**.\n\n"
        "Arquitectura en capas: modelo → repositorio → servicio → controlador.\n\n"
        "Tarea T02.03 — Universidad Politécnica Salesiana."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(categoria_controller.router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"], summary="Estado del servicio")
def health():
    return {"status": "ok"}
