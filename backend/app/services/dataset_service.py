import os, uuid
import pandas as pd
from fastapi import UploadFile, HTTPException
from app.core.config import settings

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

def save_upload(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in [".csv", ".xlsx", ".xls"]:
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are allowed")
    safe_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.UPLOAD_DIR, safe_name)
    with open(path, "wb") as buffer:
        buffer.write(file.file.read())
    return path

def read_dataset(path: str) -> pd.DataFrame:
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    df = df.drop_duplicates()
    for col in df.columns:
        if df[col].dtype.kind in "biufc":
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")
    return df

def detect_columns(df: pd.DataFrame):
    cols = list(df.columns)
    lower = {c.lower(): c for c in cols}
    date_col = next((lower[k] for k in lower if any(x in k for x in ["timestamp", "datetime", "date", "month", "time"])), cols[0] if cols else None)
    target_col = next((lower[k] for k in lower if any(x in k for x in ["energy", "usage", "consumption", "kwh", "power", "load", "sales", "demand", "quantity", "revenue", "units"])), None)
    if target_col is None:
        numeric = df.select_dtypes(include="number").columns.tolist()
        target_col = numeric[0] if numeric else (cols[-1] if cols else None)
    product_col = next((lower[k] for k in lower if "device" in k or "building" in k or "meter" in k or "sensor" in k or "product" in k or "item" in k or "sku" in k), None)
    return date_col, target_col, product_col
