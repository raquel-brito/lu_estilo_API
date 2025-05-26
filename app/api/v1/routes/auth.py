from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime

from app.core.dependencies import get_db, get_current_active_user, get_current_active_admin
from app.schemas.orders import OrderCreate, OrderOut, OrderUpdate
from app.crud import orders as crud_orders

router = APIRouter(tags=["orders"])


@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Pedido criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 2,
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
                    ]
                }
            }
        }
    ),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await crud_orders.create_order(db, order, user_id=current_user.id)


@router.get(
    "/",
    response_model=List[OrderOut],
    responses={
        200: {
            "description": "Lista de pedidos",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 2,
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
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    section: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    order_id: Optional[int] = Query(None),
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
    responses={
        200: {
            "description": "Detalhes do pedido",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 2,
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
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a acessar este pedido")
    return order


@router.put(
    "/{order_id}",
    response_model=OrderOut,
    responses={
        200: {
            "description": "Pedido atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 2,
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