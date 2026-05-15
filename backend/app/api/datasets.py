from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetOut, DatasetUploadResponse
from app.services.dataset_service import save_upload, read_dataset, detect_columns

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/upload", response_model=DatasetUploadResponse)
def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    path = save_upload(file)
    df = read_dataset(path)
    if df.empty:
        raise HTTPException(status_code=400, detail="Dataset is empty")
    date_col, target_col, product_col = detect_columns(df)
    ds = Dataset(user_id=user.id, filename=file.filename or "dataset", file_path=path, rows_count=len(df), columns_count=len(df.columns), date_column=date_col, target_column=target_col, product_column=product_col)
    db.add(ds); db.commit(); db.refresh(ds)
    return {"dataset": ds, "columns": list(df.columns), "preview": df.head(10).to_dict(orient="records")}

@router.get("", response_model=list[DatasetOut])
def list_datasets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Dataset).filter(Dataset.user_id == user.id).order_by(Dataset.id.desc()).all()

@router.get("/{dataset_id}/preview")
def preview_dataset(dataset_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ds = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.user_id == user.id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = read_dataset(ds.file_path)
    return {"columns": list(df.columns), "preview": df.head(20).to_dict(orient="records")}
