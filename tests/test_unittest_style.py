import unittest
from unittest.mock import MagicMock

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate
from app.services.categoria import CategoriaServiceImpl


class TestCategoriaServiceUnittest(unittest.TestCase):
    def test_crear_invoca_save(self):
        repo = MagicMock()
        guardada = Categoria(nombre="N", descripcion="d")
        guardada.id = 7
        repo.save.return_value = guardada
        resp = CategoriaServiceImpl(repo).crear(
            CategoriaCreate(nombre="N", descripcion="d")
        )
        self.assertEqual(resp.data[0].id, 7)
        repo.save.assert_called_once()

    def test_eliminar_inexistente(self):
        repo = MagicMock()
        repo.exists_by_id.return_value = False
        resp = CategoriaServiceImpl(repo).eliminar(404)
        self.assertEqual(resp.errors[0].codigo, 404)


if __name__ == "__main__":
    unittest.main()
