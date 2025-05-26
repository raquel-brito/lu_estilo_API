import pytest
from app.schemas.user import UserCreate
from app.crud.user import crud_user
from app.db.session import async_session
import uuid

@pytest.mark.asyncio
async def test_register_user():
    async with async_session() as session:
        # Arrange
        user_data = {
            "username": f"usuario{uuid.uuid4().hex[:8]}",
            "email": f"usuario{uuid.uuid4().hex[:8]}@email.com",
            "password": "senha123",
            "is_admin": False
        }
        user_create = UserCreate(**user_data)

        # Act
        user = await crud_user.create(session, user_in=user_create)

        # Assert
        assert user.id is not None
        assert user.email == user_data["email"]
        assert user.is_admin == user_data["is_admin"]
        assert user.username == user_data["username"]

        # Clean up
        await session.delete(user)
        await session.commit()