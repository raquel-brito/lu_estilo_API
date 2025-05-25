from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    description: str
    price: float
    barcode: str
    section: str
    stock: Optional[int] = 0
    expiration_date: Optional[date] = None
    available: Optional[bool] = True
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
