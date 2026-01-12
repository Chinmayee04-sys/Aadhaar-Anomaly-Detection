import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def run_anomaly_detection(df: pd.DataFrame) -> pd.DataFrame:
    # -----------------------------
    # Basic preprocessing
    # -----------------------------
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df = df.dropna(subset=["month"])
    df = df.sort_values("month").reset_index(drop=True)

    # -----------------------------
    # Feature engineering
    # -----------------------------
    df["update_growth_rate"] = df["total_updates"].pct_change().fillna(0)
    df["rolling_avg"] = df["total_updates"].rolling(3).mean().fillna(0)
    df["trend_deviation"] = df["total_updates"] - df["rolling_avg"]

    features = ["total_updates", "update_growth_rate", "trend_deviation"]
    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # -----------------------------
    # Isolation Forest
    # -----------------------------
    model = IsolationForest(
        n_estimators=200,
        contamination=0.15,
        random_state=42
    )

    df["anomaly_flag"] = model.fit_predict(X_scaled)
    df["anomaly"] = df["anomaly_flag"].map({1: "Normal", -1: "Anomaly"})

    # -----------------------------
    # Severity score & level
    # -----------------------------
    df["severity_score"] = (
        abs(df["update_growth_rate"]) * 100 +
        abs(df["trend_deviation"]) / df["total_updates"].mean() * 100
    ).round(2)

    def severity_level(score):
        if score >= 60:
            return "High"
        elif score >= 30:
            return "Medium"
        return "Low"

    df["severity_level"] = df["severity_score"].apply(severity_level)

    # -----------------------------
    # Anomaly type
    # -----------------------------
    def anomaly_type(row):
        if row["update_growth_rate"] > 0.5:
            return "Sudden Spike in Updates"
        elif row["update_growth_rate"] < -0.3:
            return "Sudden Drop in Updates"
        elif abs(row["trend_deviation"]) > row["total_updates"] * 0.25:
            return "Unusual Volume Deviation"
        return "Irregular Pattern"

    df["anomaly_type"] = df.apply(anomaly_type, axis=1)

    # -----------------------------
    # Root cause hint
    # -----------------------------
    def root_cause_hint(a_type):
        if a_type == "Sudden Spike in Updates":
            return "Seasonal demand surge or policy-driven update campaign"
        elif a_type == "Sudden Drop in Updates":
            return "Connectivity issues or temporary centre downtime"
        elif a_type == "Unusual Volume Deviation":
            return "Device malfunction or reporting inconsistency"
        else:
            return "Normal operational fluctuation"

    df["root_cause_hint"] = df["anomaly_type"].apply(root_cause_hint)

    # -----------------------------
    # Explanation (why flagged)
    # -----------------------------
    def explain_anomaly(row):
        reasons = []
        if abs(row["update_growth_rate"]) > 0.4:
            reasons.append("High update growth rate")
        if abs(row["trend_deviation"]) > row["total_updates"] * 0.25:
            reasons.append("Large deviation from historical trend")
        if not reasons:
            reasons.append("Minor irregular variation")
        return ", ".join(reasons)

    df["explanation"] = df.apply(explain_anomaly, axis=1)

    # -----------------------------
    # Confidence score (0–100)
    # -----------------------------
    max_sev = df["severity_score"].max()
    df["confidence_score"] = (
        df["severity_score"] / max_sev * 100
    ).round(2)

    # -----------------------------
    # What changed? (month-to-month)
    # -----------------------------
    def what_changed(curr, prev):
        diff = curr["total_updates"] - prev["total_updates"]
        pct = (diff / prev["total_updates"]) * 100
        if pct > 20:
            return f"Updates increased by {pct:.1f}% compared to previous month"
        elif pct < -20:
            return f"Updates decreased by {abs(pct):.1f}% compared to previous month"
        else:
            return "Minor change compared to previous month"

    changes = []
    for i in range(len(df)):
        if i == 0:
            changes.append("No previous data for comparison")
        else:
            changes.append(what_changed(df.iloc[i], df.iloc[i - 1]))

    df["what_changed"] = changes

    # -----------------------------
    # Early-warning forecast
    # -----------------------------
    if len(df) >= 3:
        last3 = df.tail(3)
        avg_val = last3["total_updates"].mean()
        trend = last3["total_updates"].iloc[-1] - last3["total_updates"].iloc[0]
        forecast = round(avg_val + (trend / 2), 2)
    else:
        forecast = None

    df["forecast_next_month"] = forecast

    if forecast is not None:
        mean = df["total_updates"].mean()
        std = df["total_updates"].std()
        if forecast > mean + 2 * std:
            alert = "Early Warning: Possible surge in updates next month"
        elif forecast < mean - 2 * std:
            alert = "Early Warning: Possible drop in updates next month"
        else:
            alert = "No early warning detected"
    else:
        alert = "Insufficient data for forecasting"

    df["early_warning_alert"] = alert

    return df
