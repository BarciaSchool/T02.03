from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.categoria import CategoriaRepository
from app.services.categoria import CategoriaService, CategoriaServiceImpl


def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
    return CategoriaServiceImpl(CategoriaRepository(db))
