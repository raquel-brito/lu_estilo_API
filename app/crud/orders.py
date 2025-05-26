from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import and_

from typing import List, Optional
from datetime import datetime

from app.db.models.orders import Order, OrderItem
from app.db.models.products import Product
from app.schemas.orders import OrderCreate, OrderItemCreate, OrderUpdate

async def create_order(db: AsyncSession, order_create: OrderCreate, client_id: int):
    order_items = []

    for item in order_create.items:
        result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto {item.product_id} não encontrado")

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para o produto {product.description}"
            )

        product.stock -= item.quantity
        order_items.append(OrderItem(product_id=product.id, quantity=item.quantity, price=product.price))

    order = Order(client_id=client_id, status="Pendente", items=order_items)

    db.add(order)
    await db.commit()
    await db.refresh(order)

    stmt = select(Order).options(joinedload(Order.items)).where(Order.id == order.id)
    result = await db.execute(stmt)
    created_order = result.unique().scalar_one()

    return created_order

async def get_order(db: AsyncSession, order_id: int):
    stmt = select(Order).options(joinedload(Order.items)).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.unique().scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

async def list_orders(
    db,
    client_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    section: Optional[str] = None,
    status: Optional[str] = None,
    order_id: Optional[int] = None,
):
    query = select(Order).options(joinedload(Order.items))
    filters = []

    if client_id is not None:
        filters.append(Order.client_id == client_id)
    if start_date:
        filters.append(Order.created_at >= start_date)
    if end_date:
        filters.append(Order.created_at <= end_date)
    if section and hasattr(Order, "section"):
        filters.append(Order.section == section)
    if status:
        filters.append(Order.status == status)
    if order_id:
        filters.append(Order.id == order_id)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    return result.unique().scalars().all()

async def update_order(db: AsyncSession, order_id: int, order_update: OrderUpdate):
    stmt = select(Order).options(joinedload(Order.items)).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order_update.status:
        order.status = order_update.status

    await db.commit()
    await db.refresh(order)
    return order

async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    await db.delete(order)
    await db.commit()