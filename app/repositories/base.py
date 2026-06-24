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
