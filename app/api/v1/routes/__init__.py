from fastapi import APIRouter
from .auth import router as auth_router
from .clients import router as clients_router
from .products import router as products_router



api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(clients_router, prefix="/clients", tags=["clients"])
api_router.include_router(products_router, prefix="/products", tags=["products"])

