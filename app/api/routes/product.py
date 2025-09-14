# app/routes/product.py
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils.products import UploadImageProduct
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams
from app.schemas.product import (
    ProductInSchema,
    ProductOutSchema,
    ProductsInEmployeeSchema,
    ProductUpdateSchema,
)
from app.service.product import ProductEmployeeService, ProductsService

prodcuts = APIRouter(prefix='/products', tags=['products'])


@prodcuts.post(
    '',
    description='Create a new product with image upload',
    response_model=ProductOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_products(
    description: str = Form(...),
    value_operation: float = Form(...),
    time_to_spend: str = Form(...),
    commission: float = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        if image:
            uploader = UploadImageProduct(
                description=description,
                created_at=datetime.now(),
            )
            await uploader.save_image(image)

        # repassando o dict para o produto
        product_data = {
            'description': description,
            'value_operation': value_operation,
            'time_to_spend': time_to_spend,
            'commission': commission,
            'category': category,
        }

        data = ProductInSchema(**product_data)

        return await ProductsService(session=db).add_product(data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Erro ao criar produto: {str(e)}'
        )


@prodcuts.get(
    '',
    description='List all products',
    status_code=status.HTTP_200_OK,
)
async def list_products(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        products, metadata = await ProductsService(
            session=db
        ).list_products(pagination)
        return {'data': products, 'metadata': metadata}

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while listing products.',
        )


@prodcuts.get(
    '/{id}',
    description='Get product of id',
    status_code=status.HTTP_200_OK,
)
async def get_product(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await ProductsService(session=db).get_product(id)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while retrieving the product.',
        )


@prodcuts.put(
    '/{id}',
    description='Update product of id',
    status_code=status.HTTP_200_OK,
)
async def update_products(
    id: UUID, data: ProductUpdateSchema, db: AsyncSession = Depends(get_db)
):
    try:
        return await ProductsService(session=db).update_product(id, data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the product.',
        )


@prodcuts.delete(
    '/{id}',
    description='Delete product of id',
    status_code=status.HTTP_200_OK,
)
async def delete_products(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await ProductsService(session=db).delete_product(id)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the product.',
        )


@prodcuts.post(
    '/employee',
    description='Relation between employee and product',
    status_code=status.HTTP_201_CREATED,
)
async def add_products_employe(
    data: ProductsInEmployeeSchema, db: AsyncSession = Depends(get_db)
):
    try:
        return await ProductEmployeeService(
            session=db
        ).add_products_employees(data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while creating the product.',
        )


@prodcuts.get(
    '/employee/{id}',
    description='List all products related to employee',
    status_code=status.HTTP_200_OK,
)
async def list_products_employee(
    id: UUID, db: AsyncSession = Depends(get_db)
):
    try:
        products = await ProductEmployeeService(
            session=db
        ).list_employees_products(employee_id=id)
        return {'data': products}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while listing products.',
        )
