from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.forecast import Forecast
from app.services.forecast_service import deserialize_predictions
from app.services.report_service import create_excel_report, create_pdf_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{forecast_id}/download")
def download_report(forecast_id: int, format: str = "excel", db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    fc = db.query(Forecast).filter(Forecast.id == forecast_id, Forecast.user_id == user.id).first()
    if not fc:
        raise HTTPException(status_code=404, detail="Forecast not found")
    bundle = deserialize_predictions(fc.predictions_json)
    predictions = bundle.get("predictions", bundle) if isinstance(bundle, dict) else bundle
    predictions = [{"date": x.get("timestamp", x.get("date")), "predicted_demand": x.get("predicted_kwh", x.get("predicted_demand", 0))} for x in predictions]
    if format.lower() == "pdf":
        path = create_pdf_report(predictions, forecast_id, fc.accuracy)
        media_type = "application/pdf"
    else:
        path = create_excel_report(predictions, forecast_id)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(path, media_type=media_type, filename=path.split('/')[-1])
