from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt

from app.core.config import settings  
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from sqlalchemy.future import select

ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY  

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scopes={"admin": "Acesso total", "read:clients": "Ler clientes"}
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado",
        headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissões insuficientes",
                headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
            )

    result = await db.execute(select(User).where(User.email == username))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=[])
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

async def get_current_active_admin(
    current_user: User = Security(get_current_user, scopes=["admin"])
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permissão de admin necessária")
    return current_user
