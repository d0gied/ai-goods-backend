from abc import ABC, abstractmethod

from .db import Base, session_maker
from .repositories import GoodRepository, ImageRepository


class IUnitOfWork(ABC):
    goods: GoodRepository
    images: ImageRepository

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def refresh(self, instance: Base) -> Base:
        ...

    @abstractmethod
    def refresh_all(self, instances: list[Base]) -> list[Base]:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def __enter__(self) -> "IUnitOfWork":
        ...

    @abstractmethod
    def __exit__(self, *args) -> None:
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_maker = session_maker

    def __enter__(self) -> "UnitOfWork":
        self.session = self.session_maker()
        self.goods = GoodRepository(self.session)
        self.images = ImageRepository(self.session)
        return self

    def __exit__(self, *args) -> None:
        self.rollback()
        self.close()

    def refresh(self, instance: Base) -> Base:
        self.session.refresh(instance)
        return instance

    def refresh_all(self, instances: list[Base]) -> list[Base]:
        for instance in instances:
            self.session.refresh(instance)
        return instances

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()

    def __del__(self) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<UnitOfWork session={self.session}>"
