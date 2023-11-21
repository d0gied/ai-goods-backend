from pydantic import BaseModel
from datetime import datetime

class Good(BaseModel):
    id: str
    name: str
    loaded_at: datetime | None = None
    price: float = None
    old_price: float = None
    images: list = None
    description: str = None
    source: str = None
    url: str = None
    params: dict = None
    rating: float = None
    reviews: int = None
    article: str = None
    brand: str = None
    category: str = None
    subcategory: str = None
    subsubcategory: str = None
    seller: str = None
    seller_link: str = None
    seller_rating: float = None
    seller_reviews: int = None
    seller_offers: int = None
    seller_location: str = None
    seller_is_verified: bool = None
    seller_is_official: bool = None
    seller_is_store: bool = None

