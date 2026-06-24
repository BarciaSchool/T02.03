from abc import ABC, abstractmethod

from app.models.categoria import Categoria
from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate, CategoriaOut, CategoriaUpdate
from app.schemas.response import CategoriaResponse, ErrorRest


class CategoriaService(ABC):
    @abstractmethod
    def consultar(self) -> CategoriaResponse: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> CategoriaResponse: ...

    @abstractmethod
    def crear(self, payload: CategoriaCreate) -> CategoriaResponse: ...

    @abstractmethod
    def actualizar(self, id: int, payload: CategoriaUpdate) -> CategoriaResponse: ...

    @abstractmethod
    def eliminar(self, id: int) -> CategoriaResponse: ...


class CategoriaServiceImpl(CategoriaService):
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def consultar(self) -> CategoriaResponse:
        categorias = self.repository.find_all()
        return CategoriaResponse(
            data=[CategoriaOut.model_validate(c) for c in categorias]
        )

    def buscar_por_id(self, id: int) -> CategoriaResponse:
        categoria = self.repository.find_by_id(id)
        if categoria is None:
            return CategoriaResponse(
                errors=[ErrorRest(codigo=404, mensaje="Categoría no encontrada", campo="id")]
            )
        return CategoriaResponse(data=[CategoriaOut.model_validate(categoria)])

    def crear(self, payload: CategoriaCreate) -> CategoriaResponse:
        nueva = Categoria(nombre=payload.nombre, descripcion=payload.descripcion)
        guardada = self.repository.save(nueva)
        return CategoriaResponse(data=[CategoriaOut.model_validate(guardada)])

    def actualizar(self, id: int, payload: CategoriaUpdate) -> CategoriaResponse:
        categoria = self.repository.find_by_id(id)
        if categoria is None:
            return CategoriaResponse(
                errors=[ErrorRest(codigo=404, mensaje="Categoría no encontrada", campo="id")]
            )
        categoria.nombre = payload.nombre
        categoria.descripcion = payload.descripcion
        actualizada = self.repository.save(categoria)
        return CategoriaResponse(data=[CategoriaOut.model_validate(actualizada)])

    def eliminar(self, id: int) -> CategoriaResponse:
        if not self.repository.exists_by_id(id):
            return CategoriaResponse(
                errors=[ErrorRest(codigo=404, mensaje="Categoría no encontrada", campo="id")]
            )
        self.repository.delete_by_id(id)
        return CategoriaResponse()
