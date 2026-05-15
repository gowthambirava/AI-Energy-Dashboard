from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.schemas.forecast import ForecastRequest, ForecastOut
from app.services.dataset_service import read_dataset
from app.services.forecast_service import forecast_linear, serialize_predictions, deserialize_predictions

router = APIRouter(prefix="/forecast", tags=["Forecasting"])

@router.post("/predict", response_model=ForecastOut)
def predict(payload: ForecastRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ds = db.query(Dataset).filter(Dataset.id == payload.dataset_id, Dataset.user_id == user.id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = read_dataset(ds.file_path)
    predictions, accuracy = forecast_linear(df, payload.date_column, payload.target_column, payload.periods)
    fc = Forecast(dataset_id=ds.id, user_id=user.id, periods=payload.periods, accuracy=accuracy, predictions_json=serialize_predictions(predictions))
    db.add(fc); db.commit(); db.refresh(fc)
    ds.date_column = payload.date_column; ds.target_column = payload.target_column; ds.product_column = payload.product_column
    db.commit()
    return {"id": fc.id, "dataset_id": fc.dataset_id, "periods": fc.periods, "accuracy": fc.accuracy, "predictions": predictions, "created_at": fc.created_at}

@router.get("/history", response_model=list[ForecastOut])
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.query(Forecast).filter(Forecast.user_id == user.id).order_by(Forecast.id.desc()).limit(20).all()
    
    output = []
    for r in rows:
        bundle = deserialize_predictions(r.predictions_json)
        preds = bundle.get("predictions", bundle) if isinstance(bundle, dict) else bundle
        output.append({"id": r.id, "dataset_id": r.dataset_id, "periods": r.periods, "accuracy": r.accuracy, "predictions": preds, "created_at": r.created_at})
    return output
