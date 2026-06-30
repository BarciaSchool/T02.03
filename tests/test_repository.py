from app.models.categoria import Categoria
from app.repositories.categoria import CategoriaRepository


def _nueva(nombre="Tecnología", desc="Electrónicos"):
    return Categoria(nombre=nombre, descripcion=desc)


def test_save_asigna_id(db_session):
    repo = CategoriaRepository(db_session)
    guardada = repo.save(_nueva())
    assert guardada.id is not None


def test_find_all(db_session):
    repo = CategoriaRepository(db_session)
    repo.save(_nueva("A", "a"))
    repo.save(_nueva("B", "b"))
    assert len(repo.find_all()) == 2


def test_find_by_id(db_session):
    repo = CategoriaRepository(db_session)
    g = repo.save(_nueva())
    assert repo.find_by_id(g.id).nombre == "Tecnología"


def test_find_by_id_inexistente(db_session):
    repo = CategoriaRepository(db_session)
    assert repo.find_by_id(999) is None


def test_find_all_by_id(db_session):
    repo = CategoriaRepository(db_session)
    a = repo.save(_nueva("A", "a"))
    b = repo.save(_nueva("B", "b"))
    assert len(repo.find_all_by_id([a.id, b.id])) == 2


def test_exists_by_id(db_session):
    repo = CategoriaRepository(db_session)
    g = repo.save(_nueva())
    assert repo.exists_by_id(g.id) is True
    assert repo.exists_by_id(123) is False


def test_count(db_session):
    repo = CategoriaRepository(db_session)
    repo.save(_nueva("A", "a"))
    repo.save(_nueva("B", "b"))
    assert repo.count() == 2


def test_save_all(db_session):
    repo = CategoriaRepository(db_session)
    res = repo.save_all([_nueva("A", "a"), _nueva("B", "b")])
    assert len(res) == 2
    assert repo.count() == 2


def test_delete(db_session):
    repo = CategoriaRepository(db_session)
    g = repo.save(_nueva())
    repo.delete(g)
    assert repo.count() == 0


def test_delete_by_id(db_session):
    repo = CategoriaRepository(db_session)
    g = repo.save(_nueva())
    repo.delete_by_id(g.id)
    assert repo.find_by_id(g.id) is None


def test_delete_all(db_session):
    repo = CategoriaRepository(db_session)
    repo.save(_nueva("A", "a"))
    repo.save(_nueva("B", "b"))
    repo.delete_all()
    assert repo.count() == 0
