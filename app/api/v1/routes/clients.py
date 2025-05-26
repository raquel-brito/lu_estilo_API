from fastapi import APIRouter, Depends, HTTPException, Query, status, Security, Body
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from app.core.dependencies import get_db, get_current_active_admin
from app.db.models.user import User
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.crud import clients as crud_clients

router = APIRouter()


@router.get(
    "/",
    response_model=List[ClientOut],
    responses={
        200: {
            "description": "Lista de clientes",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Maria Silva",
                            "email": "maria@email.com",
                            "cpf": "12345678900"
                        }
                    ]
                }
            }
        },
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "limit"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def list_clients(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None, alias="nome"),
    email: Optional[str] = Query(None),
):
    return await crud_clients.get_clients(db, skip, limit, name, email)


@router.post(
    "/",
    response_model=ClientOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Cliente criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 2,
                        "name": "João Souza",
                        "email": "joao@email.com",
                        "cpf": "98765432100"
                    }
                }
            }
        },
        400: {
            "description": "Email ou CPF já registrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Email já registrado"}
                }
            }
        },
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def create_client(
    client_in: ClientCreate = Body(
        ...,
        examples={
            "default": {
                "summary": "Exemplo de criação de cliente",
                "value": {
                    "name": "João Souza",
                    "email": "joao@email.com",
                    "cpf": "98765432100"
                }
            }
        }
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(get_current_active_admin, scopes=["admin"])
):
    if await crud_clients.get_client_by_email(db, client_in.email):
        raise HTTPException(status_code=400, detail="Email já registrado")
    if await crud_clients.get_client_by_cpf(db, client_in.cpf):
        raise HTTPException(status_code=400, detail="CPF já registrado")

    return await crud_clients.create_client(db, client_in)


@router.get(
    "/{id}",
    response_model=ClientOut,
    responses={
        200: {
            "description": "Detalhes do cliente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Maria Silva",
                        "email": "maria@email.com",
                        "cpf": "12345678900"
                    }
                }
            }
        },
        404: {"description": "Cliente não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def get_client(
    *,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    client = await crud_clients.get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.put(
    "/{id}",
    response_model=ClientOut,
    responses={
        200: {
            "description": "Cliente atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Maria Silva",
                        "email": "maria@email.com",
                        "cpf": "12345678900"
                    }
                }
            }
        },
        400: {
            "description": "Email ou CPF já registrado",
            "content": {
                "application/json": {
                    "example": {"detail": "CPF já registrado"}
                }
            }
        },
        404: {"description": "Cliente não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "cpf"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def update_client(
    *,
    id: int,
    client_in: ClientUpdate = Body(
        ...,
        examples={
            "default": {
                "summary": "Exemplo de atualização de cliente",
                "value": {
                    "name": "Maria Silva",
                    "email": "maria@email.com",
                    "cpf": "12345678900"
                }
            }
        }
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
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


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Cliente deletado com sucesso"},
        404: {"description": "Cliente não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def delete_client(
    *,
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    client = await crud_clients.get_client_by_id(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    await crud_clients.delete_client(db, client)