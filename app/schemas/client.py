from pydantic import BaseModel, EmailStr, Field, validator

class ClientBase(BaseModel):
    name: str= Field(example="Maria da Silva")
    email: EmailStr = Field(example="maria@cliente.com")
    cpf: str = Field(min_length=11, max_length=11, pattern=r"^\d{11}$", example="12345678900")  # CPF com 11 dígitos numéricos
    phone: str | None = None

@validator("phone")
def validate_phone(cls, v):
        if v and not v.startswith("+"):
            raise ValueError("O telefone deve começar com + e o código do país, ex: +5511999998888")
        return v

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int = Field(example=1)

    class Config:
        orm_mode = True
