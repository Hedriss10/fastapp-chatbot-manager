from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base exception para a aplicação."""

    def __init__(
        self, status_code: int, detail: str, headers: dict | None = None
    ):
        super().__init__(
            status_code=status_code, detail=detail, headers=headers
        )


class DatabaseError(AppException):
    """Erro genérico de banco de dados."""

    def __init__(self, detail: str = 'Erro interno no banco de dados'):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class InvalidPaginationError(AppException):
    """Erro quando os parâmetros de paginação são inválidos."""

    def __init__(self, detail: str = 'Parâmetros de paginação inválidos'):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class ExceptionsValueErro(AppException):
    """Retonro de value erro para o sqlalchemy"""

    def __init__(self, value_erro: str):
        self.value_erro = value_erro
