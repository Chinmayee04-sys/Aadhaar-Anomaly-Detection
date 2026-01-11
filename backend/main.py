from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import os
from pathlib import Path

from model.anomaly_model import run_anomaly_detection
from scheduler import start_scheduler

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------
app = FastAPI(
    title="Aadhaar Anomaly Detection Backend",
    description="Backend service for detecting anomalies in Aadhaar enrolment and update data",
    version="1.0"
)

# ----------------------------------------------------
# Paths
# ----------------------------------------------------
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

UPLOADED_DATA_PATH = DATA_DIR / "uploaded_data.csv"
ANOMALY_REPORT_PATH = OUTPUT_DIR / "aadhaar_anomaly_report.csv"

# ----------------------------------------------------
# Startup Event (Scheduler)
# ----------------------------------------------------
@app.on_event("startup")
def startup_event():
    """
    Starts the monthly anomaly detection scheduler
    """
    start_scheduler()

# ----------------------------------------------------
# Health Check
# ----------------------------------------------------
@app.get("/health")
def health_check():
    return {
        "status": "running",
        "service": "Aadhaar Anomaly Detection Backend"
    }

# ----------------------------------------------------
# Upload Data API
# ----------------------------------------------------
@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV is empty")

        df.to_csv(UPLOADED_DATA_PATH, index=False)

        return {
            "message": "Data uploaded successfully",
            "rows_received": len(df)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process uploaded file: {str(e)}"
        )

# ----------------------------------------------------
# Detect Anomalies API
# ----------------------------------------------------
@app.post("/detect-anomalies")
def detect_anomalies():
    if not UPLOADED_DATA_PATH.exists():
        raise HTTPException(
            status_code=400,
            detail="No data uploaded. Please upload CSV first using /upload-data."
        )

    try:
        df = pd.read_csv(UPLOADED_DATA_PATH)

        result_df = run_anomaly_detection(df)

        result_df.to_csv(ANOMALY_REPORT_PATH, index=False)

        anomalies_df = result_df[result_df["anomaly"] == "Anomaly"]

        return {
            "total_records": len(result_df),
            "anomalies_detected": len(anomalies_df),
            "results": anomalies_df.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Anomaly detection failed: {str(e)}"
        )
