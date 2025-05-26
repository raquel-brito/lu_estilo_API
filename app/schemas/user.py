from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., example="usuario1")
    email: EmailStr = Field(..., example="usuario1@teste.com")
    password: str = Field(..., example="senha123")

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
