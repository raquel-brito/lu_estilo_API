from fastapi import APIRouter, Depends, HTTPException, Query, status, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.dependencies import get_db, get_current_user
from app.db.models.client import Client
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.db.models.user import User


router = APIRouter()

# GET /clients com paginação e filtros
@router.get("/", response_model=List[ClientOut])
async def list_clients(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None, alias="nome"),
    email: Optional[str] = Query(None),
):
    query = db.query(Client)

    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    clients = query.offset(skip).limit(limit).all()
    return clients


# POST /clients - criar novo cliente com validação email e CPF únicos
@router.post("/clients/", response_model=ClientOut)
async def create_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["admin"])
):
    # verifica email único
    if db.query(Client).filter(Client.email == client_in.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")
    # verifica CPF único
    if db.query(Client).filter(Client.cpf == client_in.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já registrado")

    client = Client(**client_in.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


# GET /clients/{id} - obter cliente por id
@router.get("/{id}", response_model=ClientOut)
async def get_client(
    *,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client não encontrado")
    return client


# PUT /clients/{id} - atualizar cliente por id
@router.put("/{id}", response_model=ClientOut)
async def update_client(
    *,
    id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client não encontrado")

    # valida email e cpf únicos, ignorando o próprio cliente atualizado
    if client.email != client_in.email:
        if db.query(Client).filter(Client.email == client_in.email).first():
            raise HTTPException(status_code=400, detail="Email já registrado")
    if client.cpf != client_in.cpf:
        if db.query(Client).filter(Client.cpf == client_in.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já registrado")

    for key, value in client_in.dict(exclude_unset=True).items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client


# DELETE /clients/{id} - excluir cliente por id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    *,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(client)
    db.commit()
    return
