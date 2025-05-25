from pydantic import BaseModel, EmailStr, Field

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")  # CPF com 11 dígitos numéricos
 

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
