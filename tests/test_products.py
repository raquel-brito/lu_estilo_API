import pytest
from app.schemas.products import ProductCreate
from app.crud import products as crud_products
from app.db.session import async_session
from sqlalchemy import text
import uuid


@pytest.mark.asyncio
async def test_create_product():
    async with async_session() as session:
        product_data = {
            "description": "Teste Produto",
            "price": 10.5,
            "barcode": str(uuid.uuid4()),
            "section": "Testes",
            "stock": 100,
            "expiration_date": None,
            "available": True,
            "image_url": None,
        }

        product_create = ProductCreate(**product_data)
        product = await crud_products.create_product(session, product_create)

        assert product.id is not None
        assert product.description == product_data["description"]
        assert product.price == product_data["price"]

        await crud_products.delete_product(session, product)
        await session.execute(text('DELETE FROM products'))
        await session.commit()
