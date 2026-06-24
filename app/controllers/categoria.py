from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.dependencies import get_categoria_service
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from app.schemas.response import CategoriaResponse
from app.services.categoria import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("", response_model=CategoriaResponse, summary="Consultar todas las categorías")
def consultar(service: CategoriaService = Depends(get_categoria_service)):
    return service.consultar()


@router.get("/{id}", response_model=CategoriaResponse, summary="Buscar categoría por ID")
def buscar(id: int, service: CategoriaService = Depends(get_categoria_service)):
    resp = service.buscar_por_id(id)
    if resp.errors:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=resp.model_dump())
    return resp


@router.post(
    "",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una categoría",
)
def crear(payload: CategoriaCreate, service: CategoriaService = Depends(get_categoria_service)):
    return service.crear(payload)


@router.put("/{id}", response_model=CategoriaResponse, summary="Actualizar una categoría")
def actualizar(
    id: int,
    payload: CategoriaUpdate,
    service: CategoriaService = Depends(get_categoria_service),
):
    resp = service.actualizar(id, payload)
    if resp.errors:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=resp.model_dump())
    return resp


@router.delete("/{id}", response_model=CategoriaResponse, summary="Eliminar una categoría")
def eliminar(id: int, service: CategoriaService = Depends(get_categoria_service)):
    resp = service.eliminar(id)
    if resp.errors:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=resp.model_dump())
    return resp
