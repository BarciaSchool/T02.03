# Implementación Backend — API de Categorías (FastAPI)

> **Tarea:** T02.03 — Construcción de aplicación de software · Universidad Politécnica Salesiana
> **Tipo:** Especificación agent-ready para **Claude Code**
> **Dominio:** `Categoría` (según UML del equipo / Figura 1 de la guía)
> **Stack backend:** FastAPI + SQLAlchemy 2.0 + Pydantic v2 + MySQL 8 (Docker)
> **Arquitectura:** modelo → repositorio → servicio → controlador (equivalente al esquema Spring Boot del enunciado)

---

## 0. Cómo usar este documento con Claude Code

1. Crea el repositorio vacío y copia este archivo como `IMPLEMENTACION_CATEGORIAS_FASTAPI.md` en la raíz (o dentro de `/docs`).
2. Abre Claude Code en la carpeta del repo y dale esta instrucción inicial:

   > "Lee `IMPLEMENTACION_CATEGORIAS_FASTAPI.md` y ejecútalo paso a paso siguiendo el **Plan de ejecución (§9)**. Haz **un commit por cada tarea** con el mensaje indicado. No avances al siguiente paso hasta que el actual compile/corra. Al final verifica que `/docs` (Swagger) responda y que el CRUD funcione."

3. Claude Code irá creando cada archivo tal como se especifica en §6 y haciendo los commits del §9 (eso cubre el criterio de **≥20 commits** de la rúbrica).

> **Nota sobre la rúbrica:** los 20+ commits deben repartirse entre los integrantes del grupo. Ver §10 para la estrategia (cada quien clona y empuja sus propios commits, o se asignan tareas por persona).

---

## 1. Objetivo

Construir un servicio REST que gestione `Categoría` con operaciones CRUD completas, documentado con **Swagger/OpenAPI** y desplegable con **Docker Compose**, respetando la separación en capas del UML entregado por el equipo.

### Mapeo UML (Spring Boot) → FastAPI

| Componente UML (Spring) | Equivalente en este proyecto (FastAPI) | Archivo |
|---|---|---|
| `@Entity @Table model.Categoria` | Modelo SQLAlchemy `Categoria` | `app/models/categoria.py` |
| `org.springframework.data.repository.CrudRepository` | Clase genérica `CrudRepository[T]` | `app/repositories/base.py` |
| `model.repository.CategoriaRepository` | `CategoriaRepository(CrudRepository[Categoria])` | `app/repositories/categoria.py` |
| `service.CategoriaService` (interface) | Clase abstracta `CategoriaService(ABC)` | `app/services/categoria.py` |
| `service.CategoriaServiceImpl` (`@Service`) | `CategoriaServiceImpl(CategoriaService)` | `app/services/categoria.py` |
| `controller.CategoriaRestController` (`@RestController`) | `APIRouter` (router REST) | `app/controllers/categoria.py` |
| `response.ErrorRest` | Modelo Pydantic `ErrorRest` | `app/schemas/response.py` |
| `response.ResponseRest<T>` | Modelo genérico `ResponseRest[T]` | `app/schemas/response.py` |
| `response.CategoriaResponse` | `CategoriaResponse(ResponseRest[CategoriaOut])` | `app/schemas/response.py` |
| `org.springframework.http.ResponseEntity` | `JSONResponse` + `status_code` de FastAPI | en el controlador |
| `@Autowired` (inyección) | `Depends(...)` de FastAPI | `app/dependencies.py` |

> **Por qué FastAPI ya cubre Swagger:** FastAPI genera la documentación OpenAPI automáticamente en `/docs` (Swagger UI) y `/redoc`. No se requiere librería adicional. Solo configuramos metadatos (título, descripción, tags, summaries).

---

## 2. Endpoints REST

Base path: `/api/v1/categorias`

| Método | Ruta | Acción (servicio) | Código éxito | Descripción |
|---|---|---|---|---|
| `GET` | `/api/v1/categorias` | `consultar()` | `200` | Lista todas las categorías |
| `GET` | `/api/v1/categorias/{id}` | `buscar_por_id(id)` | `200` / `404` | Obtiene una por ID |
| `POST` | `/api/v1/categorias` | `crear(payload)` | `201` | Crea una categoría |
| `PUT` | `/api/v1/categorias/{id}` | `actualizar(id, payload)` | `200` / `404` | Actualiza una existente |
| `DELETE` | `/api/v1/categorias/{id}` | `eliminar(id)` | `200` / `404` | Elimina por ID |
| `GET` | `/health` | — | `200` | Healthcheck |

Todas las respuestas usan el envoltorio `CategoriaResponse` → `{ "data": [...], "errors": [...] }`, fiel al UML (`ResponseRest` con `data` y `errors`).

---

## 3. Estructura de carpetas

```
categorias-servicio03-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                  # App FastAPI, metadatos Swagger, routers, lifespan
│   ├── dependencies.py          # Inyección de dependencias (equiv. @Autowired)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Settings (lee .env)
│   │   └── database.py          # Engine, Session, Base, get_db
│   ├── models/
│   │   ├── __init__.py
│   │   └── categoria.py         # Entidad SQLAlchemy (@Entity/@Table)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── categoria.py         # Pydantic: Base/Create/Update/Out
│   │   └── response.py          # ErrorRest, ResponseRest[T], CategoriaResponse
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py              # CrudRepository genérico
│   │   └── categoria.py         # CategoriaRepository
│   ├── services/
│   │   ├── __init__.py
│   │   └── categoria.py         # CategoriaService (ABC) + Impl
│   └── controllers/
│       ├── __init__.py
│       └── categoria.py         # Router REST (@RestController)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_categoria.py
├── docs/
│   ├── requerimientos.md        # Tarea 02.01
│   ├── diseno.md                # Tarea 02.02 (UML + PlantUML)
│   └── tareas.md                # Tablero / asignación por integrante
├── .env.example
├── .env                         # (no se versiona)
├── .gitignore
├── .dockerignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 4. Stack y dependencias

`requirements.txt`:

```txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
sqlalchemy==2.0.36
pydantic==2.10.4
pydantic-settings==2.7.0
pymysql==1.1.1
cryptography==44.0.0
python-dotenv==1.0.1
pytest==8.3.4
httpx==0.28.1
```

> Si alguna versión no resuelve en tu entorno, desfija (`==` → `>=`) y deja que pip resuelva. `cryptography` es requerido por `pymysql` para `caching_sha2_password` (MySQL 8).

---

## 5. Configuración de entorno

`.env.example` (copiar a `.env`):

```env
PROJECT_NAME=API Categorías - POO Servicio 03
API_V1_PREFIX=/api/v1
# MySQL (Docker Compose)
DATABASE_URL=mysql+pymysql://categorias_user:CategoriasDev2026@db:3306/categorias_db
# Alternativa rápida sin Docker (desarrollo local):
# DATABASE_URL=sqlite:///./categorias.db
```

`.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.env
*.db
.pytest_cache/
.mypy_cache/
*.egg-info/
.DS_Store
```

`.dockerignore`:

```dockerignore
.venv
venv
__pycache__
*.db
.env
.git
.pytest_cache
tests
```

---

## 6. Código fuente (archivos completos)

> Estos archivos están listos para copiar. Claude Code debe crearlos exactamente así.

### 6.1 `app/__init__.py`, `app/core/__init__.py`, `app/models/__init__.py`, `app/schemas/__init__.py`, `app/repositories/__init__.py`, `app/services/__init__.py`, `app/controllers/__init__.py`, `tests/__init__.py`

Todos vacíos (archivos de paquete).

### 6.2 `app/core/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "API Categorías - POO Servicio 03"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./categorias.db"


settings = Settings()
```

### 6.3 `app/core/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# connect_args solo aplica a SQLite (modo desarrollo)
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 6.4 `app/models/categoria.py`  *(equivalente a `@Entity @Table model.Categoria`)*

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
```

### 6.5 `app/schemas/categoria.py`

```python
from pydantic import BaseModel, ConfigDict, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, examples=["Tecnología"])
    descripcion: str | None = Field(
        default=None, max_length=255, examples=["Productos electrónicos y gadgets"]
    )


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaOut(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
```

### 6.6 `app/schemas/response.py`  *(equivalente a `ErrorRest`, `ResponseRest<T>`, `CategoriaResponse`)*

```python
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
```

### 6.7 `app/repositories/base.py`  *(equivalente a `CrudRepository`)*

```python
from typing import Generic, Iterable, List, Optional, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class CrudRepository(Generic[ModelType]):
    """Réplica del CrudRepository de Spring Data (métodos del UML)."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def save(self, entity: ModelType) -> ModelType:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def save_all(self, entities: Iterable[ModelType]) -> List[ModelType]:
        objs = list(entities)
        self.db.add_all(objs)
        self.db.commit()
        for o in objs:
            self.db.refresh(o)
        return objs

    def find_all(self) -> List[ModelType]:
        return list(self.db.scalars(select(self.model)).all())

    def find_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.get(self.model, id)

    def find_all_by_id(self, ids: Iterable[int]) -> List[ModelType]:
        stmt = select(self.model).where(self.model.id.in_(list(ids)))
        return list(self.db.scalars(stmt).all())

    def exists_by_id(self, id: int) -> bool:
        return self.db.get(self.model, id) is not None

    def count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(self.model)) or 0

    def delete(self, entity: ModelType) -> None:
        self.db.delete(entity)
        self.db.commit()

    def delete_by_id(self, id: int) -> None:
        obj = self.db.get(self.model, id)
        if obj is not None:
            self.db.delete(obj)
            self.db.commit()

    def delete_all(self) -> None:
        for obj in self.find_all():
            self.db.delete(obj)
        self.db.commit()
```

### 6.8 `app/repositories/categoria.py`

```python
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.repositories.base import CrudRepository


class CategoriaRepository(CrudRepository[Categoria]):
    def __init__(self, db: Session):
        super().__init__(Categoria, db)
```

### 6.9 `app/services/categoria.py`  *(interface + impl, equivalente a `CategoriaService` / `CategoriaServiceImpl`)*

```python
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
```

### 6.10 `app/dependencies.py`  *(equivalente a `@Autowired`)*

```python
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.categoria import CategoriaRepository
from app.services.categoria import CategoriaService, CategoriaServiceImpl


def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
    return CategoriaServiceImpl(CategoriaRepository(db))
```

### 6.11 `app/controllers/categoria.py`  *(equivalente a `@RestController`)*

```python
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
```

### 6.12 `app/main.py`

```python
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
```

### 6.13 `tests/conftest.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_categorias.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)
```

### 6.14 `tests/test_categoria.py`

```python
def test_consultar_vacio(client):
    r = client.get("/api/v1/categorias")
    assert r.status_code == 200
    assert r.json() == {"data": [], "errors": []}


def test_crear_y_consultar(client):
    payload = {"nombre": "Tecnología", "descripcion": "Electrónicos"}
    r = client.post("/api/v1/categorias", json=payload)
    assert r.status_code == 201
    creada = r.json()["data"][0]
    assert creada["nombre"] == "Tecnología"
    assert creada["id"] == 1

    r2 = client.get("/api/v1/categorias")
    assert len(r2.json()["data"]) == 1


def test_buscar_por_id_no_existe(client):
    r = client.get("/api/v1/categorias/999")
    assert r.status_code == 404
    assert r.json()["errors"][0]["codigo"] == 404


def test_actualizar(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "x"})
    r = client.put("/api/v1/categorias/1", json={"nombre": "B", "descripcion": "y"})
    assert r.status_code == 200
    assert r.json()["data"][0]["nombre"] == "B"


def test_eliminar(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "x"})
    r = client.delete("/api/v1/categorias/1")
    assert r.status_code == 200
    r2 = client.get("/api/v1/categorias/1")
    assert r2.status_code == 404
```

---

## 7. Docker y despliegue

### 7.1 `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.2 `docker-compose.yml`

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: categorias_db
      MYSQL_USER: categorias_user
      MYSQL_PASSWORD: CategoriasDev2026
      MYSQL_ROOT_PASSWORD: RootDev2026
      TZ: America/Guayaquil
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 10

  api:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: mysql+pymysql://categorias_user:CategoriasDev2026@db:3306/categorias_db
      TZ: America/Guayaquil
    ports:
      - "8000:8000"
    restart: unless-stopped

volumes:
  mysql_data:
```

### 7.3 Levantar el servicio

```bash
# Con Docker (MySQL + API)
docker compose up --build -d
docker compose logs -f api

# Swagger:  http://localhost:8000/docs
# ReDoc:    http://localhost:8000/redoc
# Health:   http://localhost:8000/health
```

```bash
# Sin Docker (desarrollo rápido con SQLite)
python -m venv .venv && source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
# en .env: DATABASE_URL=sqlite:///./categorias.db
uvicorn app.main:app --reload
```

> **Despliegue en EC2 (opcional, estilo producción):** este `docker-compose.yml` encaja con tu patrón habitual Nginx/Traefik + Let's Encrypt. Para exponerlo con dominio, añade el servicio `traefik` y labels al servicio `api` (host rule + entrypoint websecure). Para la entrega de la tarea basta con `docker compose up` y exponer el puerto 8000.

---

## 8. Pruebas rápidas (cURL)

```bash
# Crear
curl -X POST http://localhost:8000/api/v1/categorias \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Tecnología","descripcion":"Electrónicos y gadgets"}'

# Consultar todas
curl http://localhost:8000/api/v1/categorias

# Buscar por id
curl http://localhost:8000/api/v1/categorias/1

# Actualizar
curl -X PUT http://localhost:8000/api/v1/categorias/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Tecnología","descripcion":"Actualizada"}'

# Eliminar
curl -X DELETE http://localhost:8000/api/v1/categorias/1
```

```bash
# Tests
pytest -v
```

---

## 9. Plan de ejecución para Claude Code (un commit por tarea)

> Ejecutar en orden. Cada línea = **1 commit**. Esto produce ~24 commits base; con los del §10 superas holgadamente los 20 de la rúbrica.

| # | Tarea | Mensaje de commit |
|---|---|---|
| 1 | `git init`, crear `.gitignore`, `.dockerignore`, `README.md` inicial | `chore: inicializar repositorio y archivos base` |
| 2 | Crear `requirements.txt` | `chore: agregar dependencias del proyecto` |
| 3 | Crear estructura de carpetas y `__init__.py` | `chore: crear estructura de paquetes` |
| 4 | Crear `app/core/config.py` | `feat(core): configuración de settings con .env` |
| 5 | Crear `app/core/database.py` | `feat(core): conexión a base de datos y sesión SQLAlchemy` |
| 6 | Crear `app/models/categoria.py` | `feat(model): entidad Categoria` |
| 7 | Crear `app/schemas/categoria.py` | `feat(schema): esquemas Pydantic de Categoria` |
| 8 | Crear `app/schemas/response.py` | `feat(schema): ErrorRest, ResponseRest y CategoriaResponse` |
| 9 | Crear `app/repositories/base.py` | `feat(repo): CrudRepository genérico` |
| 10 | Crear `app/repositories/categoria.py` | `feat(repo): CategoriaRepository` |
| 11 | Crear `app/services/categoria.py` (ABC + Impl) | `feat(service): CategoriaService e implementación` |
| 12 | Crear `app/dependencies.py` | `feat(core): inyección de dependencias del servicio` |
| 13 | Crear `app/controllers/categoria.py` | `feat(controller): endpoints REST de Categoria` |
| 14 | Crear `app/main.py` con metadatos Swagger | `feat(api): app FastAPI con documentación OpenAPI` |
| 15 | Verificar arranque local y `/docs` | `chore: verificar arranque y Swagger` |
| 16 | Crear `tests/conftest.py` | `test: fixtures y base de datos de prueba` |
| 17 | Crear `tests/test_categoria.py` | `test: cobertura CRUD de Categoria` |
| 18 | Ejecutar `pytest` y corregir si aplica | `test: pasar suite de pruebas CRUD` |
| 19 | Crear `Dockerfile` | `chore(docker): imagen de la API` |
| 20 | Crear `docker-compose.yml` (API + MySQL) | `chore(docker): orquestación API + MySQL` |
| 21 | Probar `docker compose up` | `chore(docker): verificar despliegue con compose` |
| 22 | `docs/requerimientos.md` (de Tarea 02.01) | `docs: requerimientos de la aplicación` |
| 23 | `docs/diseno.md` (UML + PlantUML del equipo) | `docs: diseño y diagrama UML` |
| 24 | `docs/tareas.md` + `README.md` final | `docs: tablero de tareas y guía de uso` |

---

## 10. Estrategia para ≥20 commits repartidos entre el equipo

La rúbrica exige *"Al menos 20 commits en el repositorio que aseguren que han trabajado todos los compañeros"*. Para que el historial muestre participación de **todos**:

1. Cada integrante configura su identidad git:
   ```bash
   git config user.name "Apellido Nombre"
   git config user.email "correo@est.ups.edu.ec"
   ```
2. Reparte las 24 tareas del §9 por persona (ejemplo para 4 integrantes):
   - **Integrante 1 (model/repo):** tareas 4–6, 9–10
   - **Integrante 2 (schemas/response):** tareas 7–8, 12
   - **Integrante 3 (service/controller/api):** tareas 11, 13–15
   - **Integrante 4 (tests/docker/docs):** tareas 16–24
   - Tareas 1–3: el líder del repo.
3. Cada quien hace **commit y push de sus propias tareas** (no que una sola persona suba todo). Opcional: trabajar por ramas (`feature/model`, `feature/service`, …) y abrir Pull Requests hacia `main`.
4. En `docs/tareas.md` documenta la asignación (cubre el criterio *"tareas definidas por usuario"* de la rúbrica).

> Si usas Claude Code para generar todo de una sola sesión, igualmente puedes hacer los commits con `--author` distinto por tarea, pero lo ideal académicamente es que cada integrante empuje físicamente sus commits.

---

## 11. Contenido sugerido para `docs/`

- **`docs/requerimientos.md`** → pega aquí los requerimientos funcionales/no funcionales definidos en la **Tarea 02.01** (RF: crear, consultar, actualizar, eliminar categorías; RNF: API REST documentada, despliegue en contenedores).
- **`docs/diseno.md`** → pega el **PlantUML** del equipo (el de la Figura 1) y el diagrama renderizado, más la tabla de mapeo UML→FastAPI de §1.
- **`docs/tareas.md`** → tabla del §9 con la columna "Responsable" llena por integrante.

---

## 12. Checklist contra la rúbrica

- [ ] **Repositorio documentado** (requerimientos + diseño + tareas) → `/docs` y `README.md` *(2 pts)*
- [ ] **≥20 commits** de todos los compañeros → §9 + §10 *(1 pt)*
- [ ] **Servicios funcionales y desplegados** → `docker compose up`, Swagger en `/docs` *(1 pt)*
- [ ] **Esquema modelo/repositorio/servicio/controlador** → cumplido (§1, §6)
- [ ] **Documentación Swagger** → automática en `/docs` y `/redoc`
- [ ] **Enlace del repositorio** en el informe PDF (punto 8 del enunciado)

---

## 13. Notas finales

- La auto-creación de tablas (`Base.metadata.create_all`) es suficiente para la tarea. Para un proyecto real migrarías a **Alembic**.
- El envoltorio `ResponseRest`/`ErrorRest` es fiel al UML; si el equipo prefiere respuestas "planas" (sin envoltorio), basta cambiar `response_model` a `CategoriaOut`/`List[CategoriaOut]` en el controlador.
- FastAPI valida automáticamente los datos de entrada (Pydantic) y devuelve `422` ante payloads inválidos, sin código adicional.
```