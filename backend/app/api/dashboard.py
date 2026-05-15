from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.services.dataset_service import read_dataset
from app.services.forecast_service import deserialize_predictions

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/analytics")
def analytics(dataset_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ds_query = db.query(Dataset).filter(Dataset.user_id == user.id)
    ds = ds_query.filter(Dataset.id == dataset_id).first() if dataset_id else ds_query.order_by(Dataset.id.desc()).first()
    if not ds:
        return {"total_sales": 0, "monthly_sales": [], "forecast_accuracy": 0, "top_products": [], "datasets_count": 0, "forecasts_count": 0, "forecast_trend": []}
    df = read_dataset(ds.file_path)
    target = ds.target_column
    date = ds.date_column
    total_sales = 0
    monthly_sales = []
    top_products = []
    if target and target in df.columns:
        df[target] = df[target].astype(float)
        total_sales = round(float(df[target].sum()), 2)
        if date and date in df.columns:
            df[date] = __import__('pandas').to_datetime(df[date], errors='coerce')
            temp = df.dropna(subset=[date]).copy()
            temp['month'] = temp[date].dt.strftime('%Y-%m')
            monthly_sales = temp.groupby('month')[target].sum().reset_index().to_dict(orient='records')
        if ds.product_column and ds.product_column in df.columns:
            top_products = df.groupby(ds.product_column)[target].sum().sort_values(ascending=False).head(5).reset_index().to_dict(orient='records')
    fc = db.query(Forecast).filter(Forecast.user_id == user.id, Forecast.dataset_id == ds.id).order_by(Forecast.id.desc()).first()
    forecast_trend = deserialize_predictions(fc.predictions_json) if fc else []
    return {"total_sales": total_sales, "monthly_sales": monthly_sales, "forecast_accuracy": fc.accuracy if fc else 0, "top_products": top_products, "datasets_count": ds_query.count(), "forecasts_count": db.query(Forecast).filter(Forecast.user_id == user.id).count(), "forecast_trend": forecast_trend}
