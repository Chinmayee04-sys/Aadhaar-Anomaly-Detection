from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import os

from model.anomaly_model import run_anomaly_detection

app = FastAPI(
    title="Aadhaar Anomaly Detection Backend",
    version="1.0.0"
)

DATA_PATH = "data/uploaded_data.csv"


@app.get("/health")
def health_check():
    return {"status": "Backend running successfully"}


@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)

        return {
            "message": "Data uploaded successfully",
            "rows_received": len(df)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/detect-anomalies")
def detect_anomalies():
    try:
        if not os.path.exists(DATA_PATH):
            raise HTTPException(
                status_code=400,
                detail="No dataset uploaded. Upload data first."
            )

        df = pd.read_csv(DATA_PATH)
        result_df = run_anomaly_detection(df)

        anomalies = result_df[result_df["anomaly_flag"] == -1]

        response = {
            "total_records": len(result_df),
            "anomalies_detected": len(anomalies),
            "results": anomalies[[
                "month",
                "total_updates",
                "anomaly_type",
                "severity_level",
                "severity_score",
                "confidence_score",
                "what_changed",
                "root_cause_hint",
                "early_warning_alert"
            ]].to_dict(orient="records")
        }

        return response

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
