from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    periods = Column(Integer, default=30)
    accuracy = Column(Float, default=0)
    predictions_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
