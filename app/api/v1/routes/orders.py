from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime

from app.core.dependencies import get_db, get_current_active_user, get_current_active_admin
from app.schemas.orders import OrderCreate, OrderOut, OrderUpdate
from app.crud import orders as crud_orders

router = APIRouter(tags=["orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await crud_orders.create_order(db, order, user_id=current_user.id)


@router.get("/", response_model=List[OrderOut])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    section: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    order_id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
):
    
    return await crud_orders.list_orders(db, start_date, end_date, section, status, order_id, client_id)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    order = await crud_orders.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a acessar este pedido")

    return order


@router.put("/{order_id}", response_model=OrderOut)
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


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    order = await crud_orders.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    await crud_orders.delete_order(db, order_id)
