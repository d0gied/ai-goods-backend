from pydantic import Field

from .base import AddSchemaType, DeleteSchemaType, UpdateSchemaType


class AddGoodSchema(AddSchemaType):
    name: str = Field(None, description="Good name")
    price: float = Field(None, description="Price")
    images: list[str] = Field(None, description="List of image URLs")
    description: str = Field(None, description="Description")
    source: str = Field(None, description="Source")
    url: str = Field(None, description="URL")
    rating: float = Field(None, description="Rating")
    reviews: int = Field(None, description="Number of reviews")


class UpdateGoodSchema(UpdateSchemaType):
    name: str = Field(None, description="Good name")
    price: float = Field(None, description="Price")
    images: list[str] = Field(None, description="List of image URLs")
    description: str = Field(None, description="Description")
    source: str = Field(None, description="Source")
    url: str = Field(None, description="URL")
    rating: float = Field(None, description="Rating")
    reviews: int = Field(None, description="Number of reviews")

    is_active: bool = Field(None, description="Is good active")
    is_processed: bool = Field(None, description="Is good processed")


class UpdateGoodEmbeddingsSchema(UpdateSchemaType):
    name_embedding: list[float] = Field(None, description="Name embedding vector")
    image_embedding: list[float] = Field(None, description="Image embedding vector")
    name_image_embedding: list[float] = Field(
        None, description="Name-image embedding vector"
    )
