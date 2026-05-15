from pydantic import BaseModel
from datetime import datetime
from typing import Any

class DatasetOut(BaseModel):
    id: int
    filename: str
    rows_count: int
    columns_count: int
    date_column: str | None = None
    target_column: str | None = None
    product_column: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True

class DatasetUploadResponse(BaseModel):
    dataset: DatasetOut
    columns: list[str]
    preview: list[dict[str, Any]]
