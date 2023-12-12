from pydantic import Field

from .base import AddSchemaType, DeleteSchemaType, UpdateSchemaType


class AddGoodSchema(AddSchemaType):
    name: str = Field(None, description="Good name")
    price: float | None = Field(None, description="Price")
    images: list[str] | None = Field(None, description="List of image URLs")
    description: str | None = Field(None, description="Description")
    source: str | None = Field(None, description="Source")
    source_id: str | None = Field(None, description="Source ID")
    url: str | None = Field(None, description="URL")
    rating: float | None = Field(None, description="Rating")
    reviews: int | None = Field(None, description="Number of reviews")

    is_active: bool | None = Field(None, description="Is good active")
    is_processed: bool | None = Field(None, description="Is good processed")


class UpdateGoodSchema(UpdateSchemaType):
    name: str | None = Field(None, description="Good name")
    price: float | None = Field(None, description="Price")
    images: list[str] | None = Field(None, description="List of image URLs")
    description: str | None = Field(None, description="Description")
    source: str | None = Field(None, description="Source")
    url: str | None = Field(None, description="URL")
    rating: float | None = Field(None, description="Rating")
    reviews: int | None = Field(None, description="Number of reviews")

    is_active: bool | None = Field(None, description="Is good active")
    is_processed: bool | None = Field(None, description="Is good processed")


class UpdateGoodEmbeddingsSchema(UpdateSchemaType):
    name_embedding: list[float] = Field(None, description="Name embedding vector")
    image_embedding: list[float] = Field(None, description="Image embedding vector")
    name_image_embedding: list[float] = Field(
        None, description="Name-image embedding vector"
    )
    is_processed: bool | None = Field(None, description="Is good processed")
    is_active: bool | None = Field(None, description="Is good active")
