# app/routes/product.py

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.product import ProdudtCore
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams
from app.schemas.product import (
    ProductEmployeeInSchema,
    ProductInSchema,
    ProductOutSchema,
    ProductUpdateSchema,
)

prodcuts = APIRouter(prefix="/products", tags=["products"])


@prodcuts.post(
    "",
    description="Create a new product",
    response_model=ProductOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_products(data: ProductInSchema, db: Session = Depends(get_db)):
    try:
        return await ProdudtCore.add_product(data, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the product.",
        )


@prodcuts.get(
    "",
    description="List all products",
    status_code=status.HTTP_200_OK,
)
async def list_products(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    try:
        products, metadata = await ProdudtCore.list_products(pagination, db)
        return {"data": products, "metadata": metadata}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while listing products.",
        )


@prodcuts.get(
    "/{id}", description="Get product of id", status_code=status.HTTP_200_OK
)
async def get_product(id: int, db: Session = Depends(get_db)):
    try:
        return await ProdudtCore.get_product(id, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print("Coletando o erro do", e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while retrieving the product.",
        )


@prodcuts.put(
    "/{id}",
    description="Update product of id",
    status_code=status.HTTP_200_OK,
)
async def update_products(
    id: int, data: ProductUpdateSchema, db: Session = Depends(get_db)
):
    try:
        return await ProdudtCore.update_product(id, data, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print("Coletando o erro", e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while updating the product.",
        )


@prodcuts.delete(
    "/{id}",
    description="Delete product of id",
    status_code=status.HTTP_200_OK,
)
async def delete_products(id: int, db: Session = Depends(get_db)):
    try:
        return await ProdudtCore.delete_product(id, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print("Coletando o erro", e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while deleting the product.",
        )


@prodcuts.post(
    "/employee",
    description="Relation between employee and product",
    status_code=status.HTTP_201_CREATED,
)
async def add_products_employe(
    data: ProductEmployeeInSchema, db: Session = Depends(get_db)
):
    try:
        return await ProdudtCore.add_products_employe(data, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the product.",
        )
