# Requerimientos — API de Categorías

> Tarea 02.01 — Universidad Politécnica Salesiana

## Requerimientos funcionales (RF)

| ID | Requerimiento | Endpoint |
|----|---------------|----------|
| RF-01 | El sistema debe permitir **crear** una categoría con nombre y descripción. | `POST /api/v1/categorias` |
| RF-02 | El sistema debe permitir **consultar** todas las categorías registradas. | `GET /api/v1/categorias` |
| RF-03 | El sistema debe permitir **buscar** una categoría por su identificador. | `GET /api/v1/categorias/{id}` |
| RF-04 | El sistema debe permitir **actualizar** los datos de una categoría existente. | `PUT /api/v1/categorias/{id}` |
| RF-05 | El sistema debe permitir **eliminar** una categoría por su identificador. | `DELETE /api/v1/categorias/{id}` |
| RF-06 | El sistema debe responder con un código `404` cuando la categoría no exista. | — |

## Requerimientos no funcionales (RNF)

| ID | Requerimiento |
|----|---------------|
| RNF-01 | La API debe ser **REST** y exponer documentación interactiva (Swagger/OpenAPI). |
| RNF-02 | La API debe **validar** automáticamente los datos de entrada y responder `422` ante payloads inválidos. |
| RNF-03 | El servicio debe ser **desplegable en contenedores** mediante Docker Compose (API + MySQL). |
| RNF-04 | La arquitectura debe respetar la separación en capas: modelo → repositorio → servicio → controlador. |
| RNF-05 | Las respuestas deben seguir el envoltorio estándar `ResponseRest` con campos `data` y `errors`. |

## Modelo de datos — `Categoria`

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| `id` | entero | PK, autoincremental |
| `nombre` | cadena (100) | obligatorio |
| `descripcion` | cadena (255) | opcional |
