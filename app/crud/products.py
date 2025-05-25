from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Product
from app.schemas.products import ProductCreate, ProductUpdate

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product).filter(Product.id == product_id)
    )
    return result.scalars().first()

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Product).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, db_product: Product, updates: ProductUpdate):
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, db_product: Product):
    await db.delete(db_product)
    await db.commit()
