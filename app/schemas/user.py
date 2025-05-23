from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


