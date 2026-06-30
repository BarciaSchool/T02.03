from unittest.mock import MagicMock

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from app.services.categoria import CategoriaServiceImpl


def _cat(id=1, nombre="Tecnología", desc="Electrónicos"):
    c = Categoria(nombre=nombre, descripcion=desc)
    c.id = id
    return c


def test_consultar():
    repo = MagicMock()
    repo.find_all.return_value = [_cat(1, "A", "a"), _cat(2, "B", "b")]
    resp = CategoriaServiceImpl(repo).consultar()
    assert len(resp.data) == 2
    assert resp.errors == []
    repo.find_all.assert_called_once()


def test_buscar_por_id_ok():
    repo = MagicMock()
    repo.find_by_id.return_value = _cat(5, "X", "x")
    resp = CategoriaServiceImpl(repo).buscar_por_id(5)
    assert resp.data[0].id == 5
    repo.find_by_id.assert_called_once_with(5)


def test_buscar_por_id_404():
    repo = MagicMock()
    repo.find_by_id.return_value = None
    resp = CategoriaServiceImpl(repo).buscar_por_id(99)
    assert resp.data == []
    assert resp.errors[0].codigo == 404


def test_crear():
    repo = MagicMock()
    repo.save.return_value = _cat(10, "Nueva", "desc")
    resp = CategoriaServiceImpl(repo).crear(
        CategoriaCreate(nombre="Nueva", descripcion="desc")
    )
    assert resp.data[0].id == 10
    repo.save.assert_called_once()


def test_actualizar_ok():
    repo = MagicMock()
    repo.find_by_id.return_value = _cat(3, "Viejo", "v")
    repo.save.return_value = _cat(3, "Nuevo", "n")
    resp = CategoriaServiceImpl(repo).actualizar(
        3, CategoriaUpdate(nombre="Nuevo", descripcion="n")
    )
    assert resp.data[0].nombre == "Nuevo"


def test_actualizar_404():
    repo = MagicMock()
    repo.find_by_id.return_value = None
    resp = CategoriaServiceImpl(repo).actualizar(
        99, CategoriaUpdate(nombre="X", descripcion="y")
    )
    assert resp.errors[0].codigo == 404


def test_eliminar_ok():
    repo = MagicMock()
    repo.exists_by_id.return_value = True
    resp = CategoriaServiceImpl(repo).eliminar(1)
    assert resp.errors == []
    repo.delete_by_id.assert_called_once_with(1)


def test_eliminar_404():
    repo = MagicMock()
    repo.exists_by_id.return_value = False
    resp = CategoriaServiceImpl(repo).eliminar(99)
    assert resp.errors[0].codigo == 404
