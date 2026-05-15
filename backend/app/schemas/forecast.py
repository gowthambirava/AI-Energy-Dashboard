from pydantic import BaseModel
from datetime import datetime
from typing import Any

class ForecastRequest(BaseModel):
    dataset_id: int
    date_column: str
    target_column: str
    product_column: str | None = None
    periods: int = 30

class ForecastOut(BaseModel):
    id: int
    dataset_id: int
    periods: int
    accuracy: float
    predictions: list[dict[str, Any]]
    created_at: datetime
