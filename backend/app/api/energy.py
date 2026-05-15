from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.services.dataset_service import read_dataset
from app.services.energy_service import forecast_energy, detect_anomalies, peak_predictions, recommendations, simulate, serialize, deserialize

router = APIRouter(prefix="/energy", tags=["AI Energy Forecasting"])

class EnergyForecastRequest(BaseModel):
    dataset_id: int
    timestamp_column: str
    usage_column: str
    device_column: str | None = None
    horizon: str = "24h"

class ScenarioRequest(BaseModel):
    forecast_id: int | None = None
    scenario: str = "peak_load_reduction"
    percent: float = 10
    cost_per_kwh: float = 8

@router.post('/train')
def train_energy_model(payload: EnergyForecastRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ds = db.query(Dataset).filter(Dataset.id == payload.dataset_id, Dataset.user_id == user.id).first()
    if not ds:
        raise HTTPException(status_code=404, detail='Dataset not found')
    df = read_dataset(ds.file_path)
    predictions, historical, accuracy = forecast_energy(df, payload.timestamp_column, payload.usage_column, payload.device_column, payload.horizon)
    anomalies = detect_anomalies(df, payload.timestamp_column, payload.usage_column)
    peaks = peak_predictions(predictions)
    recs = recommendations(predictions, anomalies)
    bundle = {"predictions": predictions, "historical": historical, "peaks": peaks, "anomalies": anomalies, "recommendations": recs, "horizon": payload.horizon}
    fc = Forecast(dataset_id=ds.id, user_id=user.id, periods=len(predictions), accuracy=accuracy, predictions_json=serialize(bundle))
    ds.date_column = payload.timestamp_column; ds.target_column = payload.usage_column; ds.product_column = payload.device_column
    db.add(fc); db.commit(); db.refresh(fc)
    return {"id": fc.id, "dataset_id": ds.id, "accuracy": accuracy, **bundle}

@router.get('/overview')
def overview(dataset_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ds_query = db.query(Dataset).filter(Dataset.user_id == user.id)
    ds = ds_query.filter(Dataset.id == dataset_id).first() if dataset_id else ds_query.order_by(Dataset.id.desc()).first()
    if not ds:
        return {"total_kwh": 0, "datasets_count": 0, "forecasts_count": 0, "device_usage": [], "hourly_usage": [], "latest": None}
    df = read_dataset(ds.file_path)
    ts, usage, dev = ds.date_column, ds.target_column, ds.product_column
    total = 0; hourly=[]; devices=[]
    if ts in df.columns and usage in df.columns:
        import pandas as pd
        df[ts]=pd.to_datetime(df[ts], errors='coerce'); df[usage]=pd.to_numeric(df[usage], errors='coerce')
        clean=df.dropna(subset=[ts,usage])
        total=round(float(clean[usage].sum()),2)
        clean['hour']=clean[ts].dt.hour
        hourly=clean.groupby('hour')[usage].sum().reset_index().to_dict(orient='records')
        if dev and dev in clean.columns:
            devices=clean.groupby(dev)[usage].sum().sort_values(ascending=False).head(8).reset_index().rename(columns={dev:'device',usage:'kwh'}).to_dict(orient='records')
    fc = db.query(Forecast).filter(Forecast.user_id == user.id, Forecast.dataset_id == ds.id).order_by(Forecast.id.desc()).first()
    latest = deserialize(fc.predictions_json) if fc else None
    return {"total_kwh": total, "datasets_count": ds_query.count(), "forecasts_count": db.query(Forecast).filter(Forecast.user_id == user.id).count(), "device_usage": devices, "hourly_usage": hourly, "latest": latest, "accuracy": fc.accuracy if fc else 0}

@router.post('/simulate')
def run_simulation(payload: ScenarioRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    fc = None
    if payload.forecast_id:
        fc = db.query(Forecast).filter(Forecast.id == payload.forecast_id, Forecast.user_id == user.id).first()
    if not fc:
        fc = db.query(Forecast).filter(Forecast.user_id == user.id).order_by(Forecast.id.desc()).first()
    if not fc:
        raise HTTPException(status_code=404, detail='No forecast found. Train a forecast first.')
    bundle = deserialize(fc.predictions_json)
    predictions = bundle.get('predictions', bundle if isinstance(bundle, list) else [])
    return simulate(predictions, payload.scenario, payload.percent, payload.cost_per_kwh)
