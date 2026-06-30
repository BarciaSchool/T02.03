# API de Categorías — FastAPI

> Tarea **T02.03** — Construcción de aplicación de software · Universidad Politécnica Salesiana
> Stack: **FastAPI + SQLAlchemy 2.0 + Pydantic v2 + MySQL 8 (Docker)**
> Arquitectura: **modelo → repositorio → servicio → controlador**

Servicio REST para la gestión de `Categoría` con operaciones **CRUD** completas,
documentado con **Swagger/OpenAPI** y desplegable con **Docker Compose**.

## Integrantes — Grupo AKETOY

| # | Apellidos y Nombres |
|---|---------------------|
| 1 | Abatte Kelly |
| 2 | Barcia Adrian |
| 3 | Huambo Cesar |
| 4 | Totoy Victor |

**Docente:** Guillermo Pizarro
**Repositorio:** https://github.com/BarciaSchool/T02.03

## Arquitectura en capas — Mapeo UML (Spring) → FastAPI

El backend replica el esquema de la **Figura 1** del enunciado (modelo → repositorio → servicio → controlador):

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

## Endpoints

Base path: `/api/v1/categorias`

| Método | Ruta | Acción | Código éxito |
|--------|------|--------|--------------|
| `GET` | `/api/v1/categorias` | Lista todas las categorías | `200` |
| `GET` | `/api/v1/categorias/{id}` | Obtiene una por ID | `200` / `404` |
| `POST` | `/api/v1/categorias` | Crea una categoría | `201` |
| `PUT` | `/api/v1/categorias/{id}` | Actualiza una existente | `200` / `404` |
| `DELETE` | `/api/v1/categorias/{id}` | Elimina por ID | `200` / `404` |
| `GET` | `/health` | Healthcheck | `200` |

Todas las respuestas usan el envoltorio `{ "data": [...], "errors": [...] }`.

## Ejecución

### Con Docker (MySQL + API)

```bash
docker compose up --build -d
docker compose logs -f api
```

- Swagger: http://localhost:8000/docs
- ReDoc:   http://localhost:8000/redoc
- Health:  http://localhost:8000/health

### Sin Docker (desarrollo rápido con SQLite)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env      # ajustar DATABASE_URL=sqlite:///./categorias.db
uvicorn app.main:app --reload
```

## Pruebas unitarias y cobertura (Tarea T02.04)

Suite de pruebas automáticas por capa, con análisis de cobertura **≥ 60%** exigido
automáticamente por `--cov-fail-under=60` (cobertura lograda: **~98%**).

```bash
pip install -r requirements-dev.txt
pytest                       # ejecuta toda la suite + reporte de cobertura
```

El reporte HTML queda en `htmlcov/index.html`.

### Frameworks de testing

| Framework | Uso en el proyecto |
|---|---|
| **Pytest** | Ejecutor principal de todas las pruebas |
| **unittest / unittest.mock** | Pruebas estilo `TestCase` y simulación de dependencias (equivalente de Mockito) |
| **pytest-mock** | Fixture `mocker` para mocks (capa de servicio) |
| **doctest** | Valida los ejemplos de los docstrings en `app/utils.py` |
| **Coverage.py** (vía `pytest-cov`) | Mide el % de cobertura y exige el umbral del 60% |

### Estrategia por capa

| Capa | Tipo de prueba | Archivo |
|---|---|---|
| Repositorio | Integración con SQLite en memoria (sesión real) | `tests/test_repository.py` |
| Servicio | Unitarias con mocks (lógica de negocio + ramas 404) | `tests/test_service.py` |
| Controlador | Integración con `TestClient` (endpoints, 404, 422) | `tests/test_controller.py` |
| Schemas | Validación de Pydantic | `tests/test_schemas.py` |
| Utilidades | Doctest + estilo `unittest.TestCase` | `tests/test_doctests.py`, `tests/test_unittest_style.py` |

## Estructura

```
app/
├── main.py            # App FastAPI, metadatos Swagger, routers, lifespan
├── dependencies.py    # Inyección de dependencias (equiv. @Autowired)
├── core/              # config.py (settings) + database.py (engine/session)
├── models/            # Entidad SQLAlchemy Categoria
├── schemas/           # Pydantic: categoria.py + response.py
├── repositories/      # CrudRepository genérico + CategoriaRepository
├── services/          # CategoriaService (ABC) + CategoriaServiceImpl
├── controllers/       # Router REST
└── utils.py           # Utilidades de dominio (con doctests)
tests/                 # conftest.py + pruebas por capa (repo/service/controller/schemas/doctest/unittest)
docs/                  # requerimientos.md, diseno.md, tareas.md
pytest.ini             # Config de pytest + cobertura (--cov-fail-under=60)
.coveragerc            # Exclusiones del análisis de cobertura
requirements-dev.txt   # Dependencias de testing
```

## Documentación

- [`docs/requerimientos.md`](docs/requerimientos.md) — requerimientos funcionales y no funcionales.
- [`docs/diseno.md`](docs/diseno.md) — arquitectura, diagrama UML (PlantUML) y mapeo Spring→FastAPI.
- [`docs/tareas.md`](docs/tareas.md) — tablero de asignación de tareas por integrante.
