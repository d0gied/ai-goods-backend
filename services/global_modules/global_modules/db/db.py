from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ..config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from .models import Base

engine = create_engine(
    url=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class SessionLocal:
    def __init__(self):
        self._session = None

    def __enter__(self):
        self._session = session_maker()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()


def get_session() -> Session:
    return SessionLocal()


def create_tables():
    Base.metadata.create_all(bind=engine)
