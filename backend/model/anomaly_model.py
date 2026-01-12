import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression


def run_anomaly_detection(df: pd.DataFrame) -> pd.DataFrame:
    # -----------------------------
    # 1. Normalize column names
    # -----------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # -----------------------------
    # 2. Resolve month column safely
    # -----------------------------
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"], errors="coerce")
    elif "date" in df.columns:
        df["month"] = pd.to_datetime(df["date"], errors="coerce")
    elif "month_year" in df.columns:
        df["month"] = pd.to_datetime(df["month_year"], errors="coerce")
    else:
        raise ValueError("No valid month/date column found in dataset")

    df = df.dropna(subset=["month"])
    df = df.sort_values("month").reset_index(drop=True)

    # -----------------------------
    # 3. Resolve total updates column
    # -----------------------------
    if "total_updates" not in df.columns:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if len(numeric_cols) == 0:
            raise ValueError("No numeric column found for update counts")
        df.rename(columns={numeric_cols[0]: "total_updates"}, inplace=True)

    # -----------------------------
    # 4. Feature engineering
    # -----------------------------
    df["rolling_avg"] = df["total_updates"].rolling(3, min_periods=1).mean()
    df["trend_deviation"] = df["total_updates"] - df["rolling_avg"]
    df["update_growth_rate"] = df["total_updates"].pct_change().fillna(0)

    features = ["total_updates", "trend_deviation", "update_growth_rate"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    # -----------------------------
    # 5. Isolation Forest
    # -----------------------------
    model = IsolationForest(
        n_estimators=200,
        contamination=0.15,
        random_state=42
    )
    df["anomaly_flag"] = model.fit_predict(X_scaled)

    # -----------------------------
    # 6. Severity score & level
    # -----------------------------
    df["severity_score"] = np.abs(df["trend_deviation"]) / (
        df["rolling_avg"] + 1e-6
    ) * 100

    def severity_level(score):
        if score >= 60:
            return "High"
        elif score >= 30:
            return "Medium"
        return "Low"

    df["severity_level"] = df["severity_score"].apply(severity_level)

    # -----------------------------
    # 7. Anomaly type
    # -----------------------------
    def anomaly_type(row):
        if row["update_growth_rate"] > 0.3:
            return "Sudden Spike in Updates"
        elif row["update_growth_rate"] < -0.3:
            return "Sudden Drop in Updates"
        elif abs(row["trend_deviation"]) > row["rolling_avg"] * 0.25:
            return "Unusual Volume Deviation"
        return "Irregular Pattern"

    df["anomaly_type"] = df.apply(anomaly_type, axis=1)

    # -----------------------------
    # 8. Explainability
    # -----------------------------
    df["what_changed"] = (
        "Change compared to previous month"
    )

    def root_cause(row):
        if row["anomaly_type"] == "Sudden Spike in Updates":
            return "Policy campaign, seasonal surge, or operational drive"
        if row["anomaly_type"] == "Sudden Drop in Updates":
            return "System downtime or regional access issues"
        return "Gradual operational variation"

    df["root_cause_hint"] = df.apply(root_cause, axis=1)

    # -----------------------------
    # 9. Confidence score
    # -----------------------------
    df["confidence_score"] = np.clip(
        100 - (df["severity_score"] / 1.2),
        40,
        95
    )

    # -----------------------------
    # 10. Early-warning forecast
    # -----------------------------
    if len(df) >= 4:
        X_time = np.arange(len(df)).reshape(-1, 1)
        y = df["total_updates"].values

        reg = LinearRegression()
        reg.fit(X_time, y)

        next_month_pred = reg.predict([[len(df)]])[0]
        last_value = df["total_updates"].iloc[-1]

        if abs(next_month_pred - last_value) / last_value > 0.25:
            df["early_warning_alert"] = "Potential abnormal pattern expected next month"
        else:
            df["early_warning_alert"] = "No early warning detected"
    else:
        df["early_warning_alert"] = "Insufficient data for forecasting"

    return df
