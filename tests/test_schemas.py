import pytest
from pydantic import ValidationError

from app.schemas.categoria import CategoriaCreate


def test_nombre_obligatorio():
    with pytest.raises(ValidationError):
        CategoriaCreate(descripcion="x")


def test_nombre_vacio_invalido():
    with pytest.raises(ValidationError):
        CategoriaCreate(nombre="", descripcion="x")


def test_descripcion_opcional():
    c = CategoriaCreate(nombre="Tecnología")
    assert c.descripcion is None
