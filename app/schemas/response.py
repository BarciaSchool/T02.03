from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

from app.schemas.categoria import CategoriaOut

T = TypeVar("T")


class ErrorRest(BaseModel):
    codigo: int
    mensaje: str
    campo: str | None = None


class ResponseRest(BaseModel, Generic[T]):
    data: List[T] = Field(default_factory=list)
    errors: List[ErrorRest] = Field(default_factory=list)


class CategoriaResponse(ResponseRest[CategoriaOut]):
    """Respuesta tipada para el recurso Categoría (data: List[Categoria])."""
    pass
