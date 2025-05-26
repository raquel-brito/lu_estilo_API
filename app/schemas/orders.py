from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int = Field(example=1)
    quantity: int = Field(example=2)

class OrderCreate(BaseModel):
    client_id: Optional[int] = Field(None, example=1, description="ID do cliente para o pedido (apenas admin pode informar)")
    items: List[OrderItemCreate]
    status: Optional[str] = Field(default="PENDENTE", example="PENDENTE")

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int = Field(example=1)
    client_id: int = Field(example=1)
    status: str = Field(example="PENDENTE")
    created_at: datetime = Field(example="2025-05-26T10:00:00")
    items: List[OrderItemOut]

    class Config:
        model_config = {"from_attributes": True}