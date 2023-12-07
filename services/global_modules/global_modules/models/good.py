from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, ConfigDict, PlainSerializer, PlainValidator
from typing_extensions import Literal, Annotated
import numpy as np

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

class GoodEmbedding(BaseModel):
    id: int = Field(..., description="Good ID")
    vector: list[float] = Field(..., description="Good embedding vector")
    model_config=ConfigDict(arbitrary_types_allowed=True)