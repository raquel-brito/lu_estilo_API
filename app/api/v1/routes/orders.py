from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime

from app.core.dependencies import get_db, get_current_active_user, get_current_active_admin
from app.schemas.orders import OrderCreate, OrderOut, OrderUpdate
from app.crud import orders as crud_orders
from app.crud import clients as crud_clients
from app.services.whatsapp import send_whatsapp_message

router = APIRouter(tags=["orders"])

@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo pedido",
    description=(
        "Cria um novo pedido para o usuário autenticado. "
        "Admins podem criar pedidos para qualquer cliente informando client_id. "
        "Usuários comuns só podem criar pedidos para si mesmos."
    ),
    responses={
        201: {
            "description": "Pedido criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "client_id": 2,
                        "status": "Pendente",
                        "items": [
                            {
                                "product_id": 10,
                                "quantity": 2,
                                "price": 99.90
                            }
                        ],
                        "created_at": "2024-05-26T15:00:00"
                    }
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
                                "loc": ["body", "items"],
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
async def create_order(
    order: OrderCreate = Body(
        ...,
        examples={
            "default": {
                "summary": "Exemplo de criação de pedido",
                "value": {
                    "items": [
                        {"product_id": 10, "quantity": 2}
                    ],
                    "client_id": 1  # Exemplo para admin
                }
            }
        }
    ),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    # Admin pode criar pedido para qualquer cliente
    if current_user.is_admin:
        if not order.client_id:
            raise HTTPException(status_code=400, detail="client_id é obrigatório para admin")
        client_id = order.client_id
    else:
        # Usuário comum só pode criar pedido para si mesmo
        client_id = current_user.id

    new_order = await crud_orders.create_order(db, order, client_id=client_id)
    # Busca o cliente para pegar o telefone
    client = await crud_clients.get_client_by_id(db, client_id)
    if client and hasattr(client, "phone") and client.phone:
        send_whatsapp_message(
            to_number=client.phone,
            message=f"Olá {client.name}, seu pedido {new_order.id} foi recebido com sucesso!"
        )
    return new_order

@router.get(
    "/",
    response_model=List[OrderOut],
    summary="Listar pedidos",
    description=(
        "Lista todos os pedidos. "
        "Admins podem ver todos os pedidos e filtrar por período, seção, status, id do pedido e cliente. "
        "Usuários autenticados só veem seus próprios pedidos."
    ),
    responses={
        200: {
            "description": "Lista de pedidos",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "client_id": 2,
                            "status": "Pendente",
                            "items": [
                                {
                                    "product_id": 10,
                                    "quantity": 2,
                                    "price": 99.90
                                }
                            ],
                            "created_at": "2024-05-26T15:00:00"
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
                                "loc": ["query", "order_id"],
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
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
    start_date: Optional[datetime] = Query(None, description="Filtrar pedidos a partir desta data"),
    end_date: Optional[datetime] = Query(None, description="Filtrar pedidos até esta data"),
    section: Optional[str] = Query(None, description="Filtrar por seção do produto"),
    status: Optional[str] = Query(None, description="Filtrar por status do pedido"),
    order_id: Optional[int] = Query(None, description="Filtrar por ID do pedido"),
):
    client_id = None if current_user.is_admin else current_user.id
    return await crud_orders.list_orders(
        db,
        client_id=client_id,
        start_date=start_date,
        end_date=end_date,
        section=section,
        status=status,
        order_id=order_id,
    )

@router.get(
    "/{order_id}",
    response_model=OrderOut,
    summary="Obter detalhes de um pedido",
    description=(
        "Retorna os detalhes de um pedido específico. "
        "Admins podem acessar qualquer pedido. "
        "Usuários autenticados só podem acessar seus próprios pedidos."
    ),
    responses={
        200: {
            "description": "Detalhes do pedido",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "client_id": 2,
                        "status": "Pendente",
                        "items": [
                            {
                                "product_id": 10,
                                "quantity": 2,
                                "price": 99.90
                            }
                        ],
                        "created_at": "2024-05-26T15:00:00"
                    }
                }
            }
        },
        404: {"description": "Pedido não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "order_id"],
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
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    order = await crud_orders.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if not current_user.is_admin and order.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a acessar este pedido")
    return order

@router.put(
    "/{order_id}",
    response_model=OrderOut,
    summary="Atualizar um pedido",
    description=(
        "Atualiza as informações de um pedido específico, incluindo o status. "
        "Apenas administradores podem atualizar pedidos."
    ),
    responses={
        200: {
            "description": "Pedido atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "client_id": 2,
                        "status": "Enviado",
                        "items": [
                            {
                                "product_id": 10,
                                "quantity": 2,
                                "price": 99.90
                            }
                        ],
                        "created_at": "2024-05-26T15:00:00"
                    }
                }
            }
        },
        404: {"description": "Pedido não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "status"],
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
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    order = await crud_orders.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return await crud_orders.update_order(db, order_id, order_update)

@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um pedido",
    description=(
        "Exclui um pedido específico. "
        "Apenas administradores podem excluir pedidos."
    ),
    responses={
        204: {"description": "Pedido deletado com sucesso"},
        404: {"description": "Pedido não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "order_id"],
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
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    order = await crud_orders.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    await crud_orders.delete_order(db, order_id)