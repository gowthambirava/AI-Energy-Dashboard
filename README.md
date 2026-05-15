# AI-Based Energy Consumption Forecasting & Optimization System

Full-stack FastAPI + React application upgraded from the previous AI demand forecasting task. Existing authentication, dataset upload, forecasting, analytics and report export features are preserved, and the app is enhanced for energy consumption forecasting, anomaly detection, peak load prediction, optimization recommendations and scenario simulation.

## Major Features

- User registration and JWT login
- CSV/Excel dataset upload with duplicate removal and missing-value handling
- Energy consumption forecasting for next 24 hours, 7 days and 30 days
- Hourly and daily time-series forecasting using regression-based ML features
- Building/device-wise analytics using `device_id`, `building_id`, meter or sensor columns
- Peak usage prediction and peak-load alerts
- Consumption anomaly detection using Isolation Forest / statistical fallback
- AI-based optimization recommendations with estimated cost savings
- Scenario simulation for increased occupancy, temperature change, device shutdown and peak-load reduction
- Advanced React dashboard with red, yellow and blue real-time application theme
- Historical vs predicted charts, device-wise analytics, anomaly highlights and forecast accuracy
- Excel/PDF forecast report export

## Dataset Format

Upload CSV or Excel with columns similar to:

```csv
timestamp,building_id,device_id,energy_kwh,temperature,occupancy
2026-01-01 09:00,Building-A,HVAC-1,71,31,110
```

Required columns:

- `timestamp` or `date` column
- `energy_kwh`, `usage`, `consumption`, `power`, `load` or similar numeric energy column

Optional columns:

- `device_id`, `building_id`, `meter_id`, `sensor_id`
- `temperature`
- `occupancy`

A testing file is included at:

```txt
backend/sample_energy_consumption.csv
```

## Backend Run Steps

```powershell
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend URL:

```txt
http://127.0.0.1:8000
```

API docs:

```txt
http://127.0.0.1:8000/docs
```

## Frontend Run Steps

Open another PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```txt
http://localhost:5173
```

## Testing Flow

1. Register a user.
2. Login.
3. Go to **Upload Data**.
4. Upload `backend/sample_energy_consumption.csv`.
5. Go to **Forecast AI**.
6. Select dataset.
7. Select:
   - timestamp column: `timestamp`
   - usage column: `energy_kwh`
   - device/building column: `device_id` or `building_id`
8. Choose horizon: next 24 hours, 7 days or 30 days.
9. Click **Train Model & Generate Forecast**.
10. Check Dashboard, Optimization, Simulation and Reports pages.

## Forecasting Methodology

The backend preprocesses timestamps, removes invalid rows, aggregates time-series data by hour or day, creates features such as hour, day of week, day, month and weekend flag, and trains a regression model to forecast future energy usage. Forecast accuracy is calculated using a holdout validation split and mean absolute error compared with average usage.

## Peak Prediction Strategy

Predicted consumption values are ranked, and the top high-load periods are marked as peak usage windows. The system generates alerts such as expected peak load around a future timestamp.

## Anomaly Detection Approach

The system uses Isolation Forest when enough rows are available. For small datasets, it falls back to z-score/statistical thresholding. Anomalies represent unusual spikes, night-time usage, sensor errors or faulty device behavior.

## Optimization Strategy

Recommendations are generated from forecast peaks, average load and anomaly results. The system suggests load shifting, shutdown scheduling, load balancing and equipment inspection, with estimated savings using cost per kWh.

## Scenario Simulation

The simulation API applies what-if factors to forecasted values and estimates:

- baseline kWh
- simulated kWh
- energy savings
- cost savings
- reduction percentage

Supported scenarios:

- peak-hour load reduction
- device shutdown
- increased occupancy
- temperature increase

## API Summary

Authentication:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

Datasets:

- `POST /api/datasets/upload`
- `GET /api/datasets`
- `GET /api/datasets/{dataset_id}/preview`

Energy AI:

- `POST /api/energy/train`
- `GET /api/energy/overview`
- `POST /api/energy/simulate`

Old forecasting/report APIs preserved:

- `POST /api/forecast/predict`
- `GET /api/forecast/history`
- `GET /api/reports/{forecast_id}/download?format=pdf`
- `GET /api/reports/{forecast_id}/download?format=excel`

## Project Structure

```txt
backend/app/api          API routes
backend/app/core         config, database, security
backend/app/models       SQLAlchemy database models
backend/app/schemas      Pydantic request/response schemas
backend/app/services     dataset, forecasting, energy ML, reports
frontend/src/pages       React pages
frontend/src/components  shared UI components
```
