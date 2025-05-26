from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    description: str = Field(example="Camiseta Polo")
    price: float = Field(example=59.90)
    barcode: str = Field(example="7891234567890")
    section: str = Field(example="Roupas Masculinas")
    stock: Optional[int] = Field(0, example=100)
    expiration_date: Optional[date] = Field(None, example="2025-12-31")
    available: Optional[bool] = True
    image_url: Optional[str] = Field(None, example="https://cdn.exemplo.com/produto.jpg")


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int = Field(example=1)

    class Config:
        model_config = {"from_attributes": True}
