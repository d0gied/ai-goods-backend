from abc import ABC, abstractmethod
from typing import Type, Union

from sqlalchemy import delete, insert, select, update

from ..db import SessionLocal
from ..models.base import Base
from ..schemas.base import AddSchemaType, UpdateSchemaType


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Union[Base, None]:
        pass

    @abstractmethod
    def get_all(self) -> list[Base]:
        pass

    @abstractmethod
    def add(self, schema: AddSchemaType) -> Base:
        pass

    @abstractmethod
    def update(self, id: int, schema: UpdateSchemaType) -> Base:
        pass

    @abstractmethod
    def delete(self, id: int) -> Base:
        pass


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None

    def get(self, id: int) -> Union[Base, None]:
        with SessionLocal() as session:
            return session.get(self.model, id)

    def get_all(self) -> list[Base]:
        with SessionLocal() as session:
            return session.query(self.model).all()

    def add(self, schema: AddSchemaType) -> Base:
        with SessionLocal() as session:
            instance = self.model(**schema.model_dump())
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance

    def update(self, id: int, schema: UpdateSchemaType) -> Base:
        with SessionLocal() as session:
            instance = session.get(self.model, id)
            for field, value in schema.model_dump().items():
                setattr(instance, field, value)
            session.commit()
            session.refresh(instance)
            return instance

    def delete(self, id: int) -> Base:
        with SessionLocal() as session:
            instance = session.get(self.model, id)
            session.delete(instance)
            session.commit()
            return instance

    def get_by_ids(self, ids: list[int]) -> list[Base]:
        with SessionLocal() as session:
            return session.query(self.model).filter(self.model.id.in_(ids)).all()
