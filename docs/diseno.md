# Diseño — API de Categorías

> Tarea 02.02 — Universidad Politécnica Salesiana

## Arquitectura en capas

```
Cliente HTTP
    │
    ▼
Controlador (APIRouter)        app/controllers/categoria.py
    │   Depends(get_categoria_service)
    ▼
Servicio (ABC + Impl)          app/services/categoria.py
    │
    ▼
Repositorio (CrudRepository)   app/repositories/{base,categoria}.py
    │
    ▼
Modelo (SQLAlchemy)            app/models/categoria.py
    │
    ▼
Base de datos (MySQL / SQLite)
```

## Diagrama de clases (PlantUML)

```plantuml
@startuml
skinparam classAttributeIconSize 0

class Categoria {
  +id: int
  +nombre: str
  +descripcion: str
}

class CrudRepository<T> {
  +save(entity): T
  +find_all(): List<T>
  +find_by_id(id): Optional<T>
  +exists_by_id(id): bool
  +delete_by_id(id): void
}

class CategoriaRepository {
  +__init__(db)
}

abstract class CategoriaService {
  +consultar(): CategoriaResponse
  +buscar_por_id(id): CategoriaResponse
  +crear(payload): CategoriaResponse
  +actualizar(id, payload): CategoriaResponse
  +eliminar(id): CategoriaResponse
}

class CategoriaServiceImpl {
  -repository: CategoriaRepository
}

class CategoriaRestController {
  +consultar()
  +buscar(id)
  +crear(payload)
  +actualizar(id, payload)
  +eliminar(id)
}

class ResponseRest<T> {
  +data: List<T>
  +errors: List<ErrorRest>
}

class ErrorRest {
  +codigo: int
  +mensaje: str
  +campo: str
}

CrudRepository <|-- CategoriaRepository
CategoriaService <|.. CategoriaServiceImpl
CategoriaServiceImpl --> CategoriaRepository
CategoriaRepository --> Categoria
CategoriaRestController --> CategoriaService
ResponseRest *-- ErrorRest
@enduml
```

## Mapeo UML (Spring Boot) → FastAPI

| Componente UML (Spring) | Equivalente FastAPI | Archivo |
|---|---|---|
| `@Entity @Table model.Categoria` | Modelo SQLAlchemy `Categoria` | `app/models/categoria.py` |
| `CrudRepository` | Clase genérica `CrudRepository[T]` | `app/repositories/base.py` |
| `CategoriaRepository` | `CategoriaRepository(CrudRepository[Categoria])` | `app/repositories/categoria.py` |
| `CategoriaService` (interface) | Clase abstracta `CategoriaService(ABC)` | `app/services/categoria.py` |
| `CategoriaServiceImpl` (`@Service`) | `CategoriaServiceImpl(CategoriaService)` | `app/services/categoria.py` |
| `CategoriaRestController` (`@RestController`) | `APIRouter` | `app/controllers/categoria.py` |
| `ErrorRest` / `ResponseRest<T>` | Modelos Pydantic | `app/schemas/response.py` |
| `ResponseEntity` | `JSONResponse` + `status_code` | controlador |
| `@Autowired` | `Depends(...)` | `app/dependencies.py` |
