from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.api import auth, datasets, forecast, dashboard, reports, energy

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Energy Consumption Forecasting API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(datasets.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(energy.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Energy Consumption Forecasting API is running", "docs": "/docs"}
