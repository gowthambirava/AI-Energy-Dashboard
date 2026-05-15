from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    rows_count = Column(Integer, default=0)
    columns_count = Column(Integer, default=0)
    date_column = Column(String(100), nullable=True)
    target_column = Column(String(100), nullable=True)
    product_column = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
