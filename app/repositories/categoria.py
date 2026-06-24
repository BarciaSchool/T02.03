from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.repositories.base import CrudRepository


class CategoriaRepository(CrudRepository[Categoria]):
    def __init__(self, db: Session):
        super().__init__(Categoria, db)
