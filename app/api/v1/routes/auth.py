from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import get_password_hash as hash_password
from app.crud.user import crud_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, RefreshTokenRequest

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

router = APIRouter()

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description=(
        "Registra um novo usuário no sistema. "
        "Valida se o email já está cadastrado. "
        "Retorna os dados do usuário criado."
    ),
    responses={
        201: {
            "description": "Usuário registrado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "usuario@email.com",
                        "is_admin": False
                    }
                }
            }
        },
        400: {
            "description": "Email já registrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Email já registrado"}
                }
            }
        },
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
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
            detail="Usuário já registrado"
        )

@router.post(
    "/login",
    summary="Autenticar usuário",
    description=(
        "Realiza a autenticação do usuário. "
        "Retorna um token JWT válido para uso nas demais rotas protegidas."
    ),
    responses={
        200: {
            "description": "Login realizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Usuário ou senha incorretos",
            "content": {
                "application/json": {
                    "example": {"detail": "Usuário ou senha incorretos"}
                }
            }
        },
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "username"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        email=user.email,
        is_admin=user.is_admin,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    "/refresh-token",
    summary="Renovar token de acesso",
    description=(
        "Recebe um refresh_token e retorna um novo access_token válido. "
        "Utilize quando o token de acesso expirar."
    ),
    responses={
        200: {
            "description": "Token renovado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Refresh token não fornecido",
            "content": {
                "application/json": {
                    "example": {"detail": "Refresh token não fornecido"}
                }
            }
        },
        401: {
            "description": "Token inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Token inválido"}
                }
            }
        },
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "refresh_token"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def refresh_token(request_data: RefreshTokenRequest):
    old_token = request_data.refresh_token
    if not old_token:
        raise HTTPException(status_code=400, detail="Refresh token não fornecido")

    try:
        payload = jwt.decode(old_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")

        new_access_token = create_access_token(
            email=username,
            is_admin=False,
            expires_delta=timedelta(minutes=60)
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get(
    "/me",
    response_model=UserOut,
    summary="Obter dados do usuário autenticado",
    description=(
        "Retorna os dados do usuário atualmente autenticado. "
        "Necessário enviar o token JWT no header Authorization."
    ),
    responses={
        200: {
            "description": "Dados do usuário autenticado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "usuario@email.com",
                        "is_admin": False
                    }
                }
            }
        },
        401: {
            "description": "Não autenticado",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        }
    }
)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user