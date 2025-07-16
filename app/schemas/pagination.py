# app/schemas/pagination.py

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    current_page: int = Field(1, ge=1)
    rows_per_page: int = Field(10, ge=1, le=100)
    order_by: Optional[str] = None
    sort_by: Optional[str] = None
    filter_by: Optional[str] = None


class BuildMetadata(BaseModel):
    total_count: int
    current_page: int
    rows_per_page: int
    total_pages: int

    def build_metadata(
        total_count: int, params: PaginationParams
    ) -> Dict[str, Any]:
        """Build metadata for the response."""
        return {
            "total_count": total_count,
            "current_page": params.current_page,
            "rows_per_page": params.rows_per_page,
            "total_pages": (total_count + params.rows_per_page - 1)
            // params.rows_per_page,
        }
