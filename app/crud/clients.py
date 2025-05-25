from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List

from app.db.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


async def get_clients(
    db: AsyncSession, skip: int = 0, limit: int = 10, name: Optional[str] = None, email: Optional[str] = None
) -> List[Client]:
    query = select(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_client_by_id(db: AsyncSession, id: int) -> Optional[Client]:
    result = await db.execute(select(Client).filter(Client.id == id))
    return result.scalars().first()


async def get_client_by_email(db: AsyncSession, email: str) -> Optional[Client]:
    result = await db.execute(select(Client).filter(Client.email == email))
    return result.scalars().first()


async def get_client_by_cpf(db: AsyncSession, cpf: str) -> Optional[Client]:
    result = await db.execute(select(Client).filter(Client.cpf == cpf))
    return result.scalars().first()


async def create_client(db: AsyncSession, client_in: ClientCreate) -> Client:
    client = Client(**client_in.dict())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client


async def update_client(db: AsyncSession, db_client: Client, client_in: ClientUpdate) -> Client:
    for key, value in client_in.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    await db.commit()
    await db.refresh(db_client)
    return db_client


async def delete_client(db: AsyncSession, db_client: Client):
    await db.delete(db_client)
    await db.commit()
