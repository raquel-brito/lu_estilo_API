import pytest
from app.schemas.orders import OrderCreate
from app.crud import orders as crud_orders
from app.crud import products as crud_products
from app.db.session import async_session
from app.schemas.products import ProductCreate
import uuid

@pytest.mark.asyncio
async def test_create_order():
    async with async_session() as session:
        # Arrange: cria um produto para usar no pedido
        product_data = {
            "name": "Produto Pedido",
            "description": "Produto para teste de pedido",
            "price": 20.0,
            "barcode": str(uuid.uuid4()),
            "section": "Pedidos",
            "stock": 50,
            "expiration_date": None,
            "available": True,
            "image_url": None,
        }
        product_create = ProductCreate(**product_data)
        product = await crud_products.create_product(session, product_create)

        order_data = {
            "client_id": 1,  # ajuste conforme necessário
            "status": "Pendente",  # ajuste conforme necessário
            "items": [
                {"product_id": product.id, "quantity": 2}
            ]
        }
        order_create = OrderCreate(**order_data)

        # Act: cria o pedido
        order = await crud_orders.create_order(session, order_create, user_id=1)

        # Assert
        assert order.id is not None
        assert order.items[0].product_id == product.id
        assert order.items[0].quantity == 2

        # Clean up
        await crud_orders.delete_order(session, order.id)
        await crud_products.delete_product(session, product)
        await session.commit()