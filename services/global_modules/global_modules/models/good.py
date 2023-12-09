from datetime import datetime
from typing import Any

import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    PlainSerializer,
    PlainValidator,
)
from typing_extensions import Annotated, Literal, NewType

from ..db.schemas.good import AddGoodSchema


class Good(BaseModel):
    id: int = Field(..., description="Good ID")
    name: str = Field(..., description="Good name")
    created_at: datetime | None = Field(None, description="Creation timestamp")
    updated_at: datetime | None = Field(None, description="Update timestamp")
    price: float | None = Field(None, description="Price")
    images: list[HttpUrl] | None = Field(None, description="List of image URLs")
    description: str | None = Field(None, description="Description")
    source: str | None = Field(None, description="Source")
    url: HttpUrl | None = Field(None, description="URL")
    rating: float | None = Field(None, description="Rating")
    reviews: int | None = Field(None, description="Number of reviews")

    def to_add_schema(self):
        return AddGoodSchema(
            name=self.name,
            price=self.price,
            images=self.images,
            description=self.description,
            source=self.source,
            url=self.url,
            rating=self.rating,
            reviews=self.reviews,
        )


GoodDumped = NewType("GoodDumped", dict[str, Any])


class GoodEmbedding(BaseModel):
    id: int = Field(..., description="Good ID")
    vector: list[float] = Field(..., description="Good embedding vector")


GoodEmbeddingDumped = NewType("GoodEmbeddingDumped", dict[str, Any])
