from fastapi import APIRouter, Depends, HTTPException, Query, status, Security
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from app.core.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.crud import clients as crud_clients


router = APIRouter()


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
    return await crud_clients.get_clients(db, skip, limit, name, email)


@router.post("/", response_model=ClientOut)
async def create_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["admin"])
):
    if await crud_clients.get_client_by_email(db, client_in.email):
        raise HTTPException(status_code=400, detail="Email já registrado")
    if await crud_clients.get_client_by_cpf(db, client_in.cpf):
        raise HTTPException(status_code=400, detail="CPF já registrado")

    return await crud_clients.create_client(db, client_in)


@router.get("/{id}", response_model=ClientOut)
async def get_client(
    *,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = await crud_clients.get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.put("/{id}", response_model=ClientOut)
async def update_client(
    *,
    id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = await crud_clients.get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if client.email != client_in.email:
        if await crud_clients.get_client_by_email(db, client_in.email):
            raise HTTPException(status_code=400, detail="Email já registrado")
    if client.cpf != client_in.cpf:
        if await crud_clients.get_client_by_cpf(db, client_in.cpf):
            raise HTTPException(status_code=400, detail="CPF já registrado")

    return await crud_clients.update_client(db, client, client_in)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    *,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = await crud_clients.get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    await crud_clients.delete_client(db, client)
