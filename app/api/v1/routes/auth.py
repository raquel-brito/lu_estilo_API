from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db
from app.crud.user import crud_user
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token
from datetime import timedelta


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
    db: AsyncSession = Depends(get_db)  
):
    
    user = await crud_user.get_by_email(db, email=form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorretos"
        )
    
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorretos"
        )
    
    
    access_token_expires = timedelta(minutes=30)  
    access_token = create_access_token(
        data={"sub": user.email},  
        expires_delta=access_token_expires
    )

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

    
    
    return {"access_token": access_token, "token_type": "bearer"}
