# Evidencia de cobertura — Tarea T02.04

Resultado de ejecutar `pytest` (con `pytest-cov`) sobre el paquete `app`.
El umbral exigido por la rúbrica es **60%**; se configura en `pytest.ini` con
`--cov-fail-under=60`, de modo que la suite **falla** si la cobertura baja de ese valor.

## Resumen

- **Pruebas ejecutadas:** 41 — todas `PASSED`.
- **Cobertura total alcanzada:** **97.84%** (umbral 60% superado).
- Reporte HTML navegable: `htmlcov/index.html` (no versionado).

## Detalle por módulo

```
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app\controllers\categoria.py       31      0   100%
app\core\config.py                  7      0   100%
app\core\database.py               13      4    69%   27-31
app\dependencies.py                 7      0   100%
app\models\categoria.py             8      0   100%
app\repositories\base.py           43      0   100%
app\repositories\categoria.py       6      0   100%
app\schemas\categoria.py           11      0   100%
app\schemas\response.py            13      0   100%
app\services\categoria.py          44      0   100%
app\utils.py                        2      0   100%
-------------------------------------------------------------
TOTAL                             185      4    98%

Required test coverage of 60% reached. Total coverage: 97.84%
```

> `app/main.py` y los `__init__.py` se excluyen del cómputo mediante `.coveragerc`.
> Las líneas 27-31 de `database.py` corresponden a `get_db()`, que en pruebas se
> sustituye por un override de la dependencia (SQLite en memoria).
