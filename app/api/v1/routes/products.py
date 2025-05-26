from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.products import ProductCreate, ProductUpdate, ProductOut
from app.crud import products as crud_products
from app.core.dependencies import get_db, get_current_active_user, get_current_active_admin

router = APIRouter(tags=["products"])


@router.get(
    "/",
    response_model=List[ProductOut],
    responses={
        200: {
            "description": "Lista de produtos",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Camiseta",
                            "description": "Camiseta 100% algodão",
                            "price": 49.90,
                            "stock": 100
                        }
                    ]
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
                                "loc": ["query", "limit"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),  
):
    return await crud_products.get_products(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Produto criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 2,
                        "name": "Calça Jeans",
                        "description": "Calça jeans azul",
                        "price": 129.90,
                        "stock": 50
                    }
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
                                "loc": ["body", "name"],
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
async def create_product(
    product: ProductCreate = Body(
        ...,
        examples={
            "default": {
                "summary": "Exemplo de criação de produto",
                "value": {
                    "name": "Calça Jeans",
                    "description": "Calça jeans azul",
                    "price": 129.90,
                    "stock": 50
                }
            }
        }
    ),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_admin),  
):
    return await crud_products.create_product(db, product)


@router.get(
    "/{product_id}",
    response_model=ProductOut,
    responses={
        200: {
            "description": "Detalhes do produto",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Camiseta",
                        "description": "Camiseta 100% algodão",
                        "price": 49.90,
                        "stock": 100
                    }
                }
            }
        },
        404: {"description": "Produto não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "product_id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def read_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),  
):
    db_product = await crud_products.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    responses={
        200: {
            "description": "Produto atualizado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Camiseta",
                        "description": "Camiseta 100% algodão - Nova descrição",
                        "price": 59.90,
                        "stock": 90
                    }
                }
            }
        },
        404: {"description": "Produto não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "price"],
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
async def update_product(
    product_id: int,
    updates: ProductUpdate = Body(
        ...,
        examples={
            "default": {
                "summary": "Exemplo de atualização de produto",
                "value": {
                    "name": "Camiseta",
                    "description": "Camiseta 100% algodão - Nova descrição",
                    "price": 59.90,
                    "stock": 90
                }
            }
        }
    ),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_admin),  # só admins
):
    db_product = await crud_products.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return await crud_products.update_product(db, db_product, updates)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Produto deletado com sucesso"},
        404: {"description": "Produto não encontrado"},
        422: {
            "description": "Erro de validação",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "product_id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_admin),  
):
    db_product = await crud_products.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await crud_products.delete_product(db, db_product)