from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pandas as pd
from pathlib import Path

from model.anomaly_model import run_anomaly_detection


# ----------------------------------------------------
# Paths
# ----------------------------------------------------
DATA_INPUT_PATH = Path("data/monthly_updates.csv")
OUTPUT_PATH = Path("outputs/aadhaar_anomaly_report.csv")


def monthly_anomaly_job():
    """
    This function runs automatically every month
    """
    print(f"[SCHEDULER] Monthly anomaly check started at {datetime.now()}")

    if not DATA_INPUT_PATH.exists():
        print("[SCHEDULER] Input data file not found. Skipping job.")
        return

    try:
        df = pd.read_csv(DATA_INPUT_PATH)

        result_df = run_anomaly_detection(df)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        result_df.to_csv(OUTPUT_PATH, index=False)

        print(
            f"[SCHEDULER] Monthly anomaly report generated successfully "
            f"({len(result_df)} records)"
        )

    except Exception as e:
        print(f"[SCHEDULER] ERROR: {str(e)}")


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run once every month (1st day, 02:00 AM)
    scheduler.add_job(
        monthly_anomaly_job,
        trigger="cron",
        day=1,
        hour=2,
        minute=0
    )

    scheduler.start()
    print("[SCHEDULER] Monthly scheduler started")
