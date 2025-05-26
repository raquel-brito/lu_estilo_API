import pytest
from app.schemas.client import ClientCreate
from app.crud import clients as crud_clients
from app.db.session import async_session
import uuid

@pytest.mark.asyncio
async def test_create_client():
    async with async_session() as session:
        # Arrange
        client_data = {
            "name": "Cliente Teste",
            "email": f"cliente{uuid.uuid4().hex[:8]}@email.com",
            "cpf": str(uuid.uuid4().int)[:11]
        }
        client_create = ClientCreate(**client_data)

        # Act
        client = await crud_clients.create_client(session, client_create)

        # Assert
        assert client.id is not None
        assert client.name == client_data["name"]
        assert client.email == client_data["email"]
        assert client.cpf == client_data["cpf"]

        # Clean up
        await crud_clients.delete_client(session, client)
        await session.commit()