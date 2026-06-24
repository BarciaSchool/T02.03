# Tablero de tareas — API de Categorías

> Asignación por integrante. Cada quien hace **commit y push de sus propias tareas**
> para evidenciar la participación de todo el equipo (criterio de la rúbrica: ≥20 commits).

## Configuración de identidad (cada integrante)

```bash
git config user.name "Apellido Nombre"
git config user.email "correo@est.ups.edu.ec"
```

## Asignación de tareas (ejemplo para 4 integrantes)

| # | Tarea | Mensaje de commit | Responsable |
|---|-------|-------------------|-------------|
| 1 | Inicializar repo, `.gitignore`, `.dockerignore`, README inicial | `chore: inicializar repositorio y archivos base` | Líder |
| 2 | `requirements.txt` | `chore: agregar dependencias del proyecto` | Líder |
| 3 | Estructura de paquetes (`__init__.py`) | `chore: crear estructura de paquetes` | Líder |
| 4 | `app/core/config.py` | `feat(core): configuración de settings con .env` | Integrante 1 |
| 5 | `app/core/database.py` | `feat(core): conexión a base de datos y sesión SQLAlchemy` | Integrante 1 |
| 6 | `app/models/categoria.py` | `feat(model): entidad Categoria` | Integrante 1 |
| 7 | `app/schemas/categoria.py` | `feat(schema): esquemas Pydantic de Categoria` | Integrante 2 |
| 8 | `app/schemas/response.py` | `feat(schema): ErrorRest, ResponseRest y CategoriaResponse` | Integrante 2 |
| 9 | `app/repositories/base.py` | `feat(repo): CrudRepository genérico` | Integrante 1 |
| 10 | `app/repositories/categoria.py` | `feat(repo): CategoriaRepository` | Integrante 1 |
| 11 | `app/services/categoria.py` | `feat(service): CategoriaService e implementación` | Integrante 3 |
| 12 | `app/dependencies.py` | `feat(core): inyección de dependencias del servicio` | Integrante 2 |
| 13 | `app/controllers/categoria.py` | `feat(controller): endpoints REST de Categoria` | Integrante 3 |
| 14 | `app/main.py` | `feat(api): app FastAPI con documentación OpenAPI` | Integrante 3 |
| 15 | Verificar arranque y `/docs` | `chore: verificar arranque y Swagger` | Integrante 3 |
| 16 | `tests/conftest.py` | `test: fixtures y base de datos de prueba` | Integrante 4 |
| 17 | `tests/test_categoria.py` | `test: cobertura CRUD de Categoria` | Integrante 4 |
| 18 | Ejecutar `pytest` | `test: pasar suite de pruebas CRUD` | Integrante 4 |
| 19 | `Dockerfile` | `chore(docker): imagen de la API` | Integrante 4 |
| 20 | `docker-compose.yml` | `chore(docker): orquestación API + MySQL` | Integrante 4 |
| 21 | Probar `docker compose up` | `chore(docker): verificar despliegue con compose` | Integrante 4 |
| 22 | `docs/requerimientos.md` | `docs: requerimientos de la aplicación` | Integrante 4 |
| 23 | `docs/diseno.md` | `docs: diseño y diagrama UML` | Integrante 4 |
| 24 | `docs/tareas.md` + README final | `docs: tablero de tareas y guía de uso` | Integrante 4 |
