from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


async def get_clients(
    db: Session, skip: int = 0, limit: int = 10, name: Optional[str] = None, email: Optional[str] = None
) -> List[Client]:
    query = db.query(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()


async def get_client_by_id(db: Session, id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.id == id).first()


async def get_client_by_email(db: Session, email: str) -> Optional[Client]:
    return db.query(Client).filter(Client.email == email).first()


async def get_client_by_cpf(db: Session, cpf: str) -> Optional[Client]:
    return db.query(Client).filter(Client.cpf == cpf).first()


async def create_client(db: AsyncSession, client_in: ClientCreate) -> Client:
    client = Client(**client_in.dict())
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client


async def update_client(db: Session, db_client: Client, client_in: ClientUpdate) -> Client:
    for key, value in client_in.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client


async def delete_client(db: Session, db_client: Client):
    db.delete(db_client)
    db.commit()
