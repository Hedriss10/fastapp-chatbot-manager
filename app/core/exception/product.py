from fastapi import status

from app.core.exception.exceptions import AppException


class ProductNotFoundError(AppException):
    """Erro quando um produto não é encontrado."""

    def __init__(self, product_id: int | None = None):
        detail = f'Produto com ID {product_id} não encontrado' if product_id else 'Produto não encontrado'
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
