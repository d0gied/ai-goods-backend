from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..types import Embedding
from .base import Base


class Good(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    price = Column(Float, index=True)
    images = Column(String)
    description = Column(String)
    source_id = Column(String)
    source = Column(String)
    url = Column(String)
    rating = Column(Integer)
    reviews = Column(Integer)

    is_active = Column(Boolean, default=True)
    is_processed = Column(Boolean, default=False)

    image_embedding = Column(Embedding, default=[0] * 512)
    name_embedding = Column(Embedding, default=[0] * 512)
    name_image_embedding = Column(Embedding, default=[0] * 512)

    def __repr__(self) -> str:
        return f"<Good {self.id}: name={self.name}, price={self.price}>"
