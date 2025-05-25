from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.crud import products as crud_products
from app.core.dependencies import get_db, get_current_active_admin

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductOut])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud_products.get_products(db, skip=skip, limit=limit)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    return await crud_products.create_product(db, product)


@router.get("/{product_id}", response_model=ProductOut)
async def read_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_product = await crud_products.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    updates: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    db_product = await crud_products.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return await crud_products.update_product(db, db_product, updates)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    db_product = await crud_products.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await crud_products.delete_product(db, db_product)
    return
