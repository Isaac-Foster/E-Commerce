from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: int
    variations: list = field(default_factory=list)
    images: list = field(default_factory=list)
    videos: list = field(default_factory=list)