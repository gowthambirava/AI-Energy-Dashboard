import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.core.config import settings

os.makedirs(settings.REPORT_DIR, exist_ok=True)

def create_excel_report(predictions, forecast_id: int) -> str:
    path = os.path.join(settings.REPORT_DIR, f"forecast_report_{forecast_id}.xlsx")
    pd.DataFrame(predictions).to_excel(path, index=False)
    return path

def create_pdf_report(predictions, forecast_id: int, accuracy: float) -> str:
    path = os.path.join(settings.REPORT_DIR, f"forecast_report_{forecast_id}.pdf")
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Demand Forecast Report")
    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Forecast ID: {forecast_id}    Accuracy: {accuracy}%")
    y -= 35
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Date")
    c.drawString(180, y, "Predicted Demand")
    y -= 20
    c.setFont("Helvetica", 10)
    for row in predictions[:35]:
        if y < 60:
            c.showPage(); y = height - 50
        c.drawString(50, y, str(row.get("date")))
        c.drawString(180, y, str(row.get("predicted_demand")))
        y -= 18
    c.save()
    return path
