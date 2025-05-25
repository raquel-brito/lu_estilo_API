from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    client_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None  

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    product_name: Optional[str]

class OrderOut(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
