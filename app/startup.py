from app.db.session import async_session
from app.db.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.future import select
import asyncio
import os

async def create_initial_admin():
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(is_admin=True))
        admin = result.scalars().first()

        if not admin:
            admin_email = os.getenv("ADMIN_EMAIL", "admin@luestilo.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

            new_admin = User(
                email=admin_email,
                username="admin",
                hashed_password=get_password_hash(admin_password),
                is_admin=True
            )
            session.add(new_admin)
            await session.commit()
            print("Admin criado automaticamente.")
