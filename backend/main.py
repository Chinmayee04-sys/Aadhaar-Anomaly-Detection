from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import os

from model.anomaly_model import run_anomaly_detection
from scheduler import start_scheduler

# -----------------------------
# App initialization
# -----------------------------
app = FastAPI(
    title="Aadhaar Anomaly Detection Backend",
    description="Backend service for detecting anomalies in Aadhaar update data",
    version="1.0.0"
)

DATA_DIR = "data"
OUTPUT_DIR = "outputs"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATA_FILE = os.path.join(DATA_DIR, "monthly_updates.csv")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "aadhaar_anomaly_report.csv")

# -----------------------------
# Startup (scheduler)
# -----------------------------
@app.on_event("startup")
def startup_event():
    start_scheduler()
    print("[SCHEDULER] Monthly scheduler started")

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "OK"}

# -----------------------------
# Upload CSV
# -----------------------------
@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        with open(DATA_FILE, "wb") as f:
            f.write(await file.read())

        df = pd.read_csv(DATA_FILE)

        if {"month", "total_updates"} - set(df.columns):
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'month' and 'total_updates' columns"
            )

        return {
            "message": "Data uploaded successfully",
            "rows_received": len(df)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Detect anomalies
# -----------------------------
@app.post("/detect-anomalies")
def detect_anomalies():
    try:
        if not os.path.exists(DATA_FILE):
            raise HTTPException(
                status_code=400,
                detail="No data uploaded. Please upload CSV first."
            )

        df = pd.read_csv(DATA_FILE)
        result_df = run_anomaly_detection(df)

        result_df.to_csv(OUTPUT_FILE, index=False)

        anomalies = result_df[result_df["anomaly"] == "Anomaly"]

        return {
            "total_records": len(result_df),
            "anomalies_detected": len(anomalies),
            "results": anomalies[
                [
                    "month",
                    "total_updates",
                    "anomaly_type",
                    "severity_level",
                    "severity_score",
                    "confidence_score",
                    "what_changed",
                    "root_cause_hint",
                    "explanation",
                    "forecast_next_month",
                    "early_warning_alert"
                ]
            ].to_dict(orient="records")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
