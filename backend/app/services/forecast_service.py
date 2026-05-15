from app.services.energy_service import forecast_energy, serialize, deserialize

# Backward-compatible names from the old demand forecasting task.
def forecast_linear(df, date_column, target_column, periods=30):
    horizon = "30d" if int(periods) >= 30 else "7d" if int(periods) >= 7 else "24h"
    predictions, historical, accuracy = forecast_energy(df, date_column, target_column, None, horizon)
    converted = [{"date": p["timestamp"], "predicted_demand": p["predicted_kwh"], "timestamp": p["timestamp"], "predicted_kwh": p["predicted_kwh"]} for p in predictions]
    return converted, accuracy

def serialize_predictions(predictions):
    return serialize(predictions)

def deserialize_predictions(text):
    return deserialize(text)
