from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class CRUDUser:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=hashed_password,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update(self, db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
        if user_in.name is not None:
            db_user.name = user_in.name
        if user_in.email is not None:
            db_user.email = user_in.email
        if user_in.password is not None:
            db_user.hashed_password = get_password_hash(user_in.password)
        if user_in.is_active is not None:
            db_user.is_active = user_in.is_active
        if user_in.is_admin is not None:
            db_user.is_admin = user_in.is_admin

        await db.commit()
        await db.refresh(db_user)
        return db_user
