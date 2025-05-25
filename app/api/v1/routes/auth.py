from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.security import verify_password, create_access_token
from app.core.security import get_password_hash as hash_password
from app.crud.user import crud_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await crud_user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    try:
        user = await crud_user.create(db, user_in=user_in)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await crud_user.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorretos"
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "scopes": ["admin"] if user.is_admin else []},
        expires_delta=access_token_expires
)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh-token")
async def refresh_token(request: Request):
    token = await request.json()
    old_token = token.get("refresh_token")
    if not old_token:
        raise HTTPException(status_code=400, detail="Refresh token não fornecido")

    try:
        payload = jwt.decode(old_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")

        new_access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=60))
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users/", response_model=UserOut)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["admin"])
):
    existing_user = await crud_user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    user_data = user_in.dict()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))

    new_user = User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user