import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def run_anomaly_detection(df: pd.DataFrame):

    # =====================================================
    # 1. Normalize column names
    # =====================================================
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # =====================================================
    # 2. Identify month column
    # =====================================================
    month_col = None
    for col in df.columns:
        if "month" in col or "period" in col or "date" in col:
            month_col = col
            break

    if month_col is None:
        raise ValueError(
            f"No month-like column found. Columns: {list(df.columns)}"
        )

    df.rename(columns={month_col: "month"}, inplace=True)

    # =====================================================
    # 3. Identify total updates column
    # =====================================================
    updates_col = None
    for col in df.columns:
        if "update" in col or "value" in col:
            updates_col = col
            break

    if updates_col is None:
        raise ValueError(
            f"No updates/value column found. Columns: {list(df.columns)}"
        )

    df.rename(columns={updates_col: "total_updates"}, inplace=True)

    # =====================================================
    # 4. Identify state / district columns (if present)
    # =====================================================
    state_col = None
    district_col = None

    for col in df.columns:
        if "state" in col:
            state_col = col
        if "district" in col:
            district_col = col

    # Standardize text
    if state_col:
        df[state_col] = df[state_col].astype(str).str.title().str.strip()
    if district_col:
        df[district_col] = df[district_col].astype(str).str.title().str.strip()

    # =====================================================
    # 5. Convert and sort by month
    # =====================================================
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df = df.dropna(subset=["month"])
    df = df.sort_values("month").reset_index(drop=True)

    # =====================================================
    # 6. Decide grouping level
    # =====================================================
    if state_col and district_col:
        group_cols = [state_col, district_col]
    elif state_col:
        group_cols = [state_col]
    else:
        group_cols = None  # National-level

    results = []

    # =====================================================
    # 7. Group-wise anomaly detection
    # =====================================================
    grouped_data = (
        df.groupby(group_cols)
        if group_cols else
        [(None, df)]
    )

    for group_key, group_df in grouped_data:

        # Skip very small groups
        if len(group_df) < 6:
            continue

        group_df = group_df.sort_values("month").copy()

        # Feature engineering
        group_df["update_growth_rate"] = group_df["total_updates"].pct_change()
        group_df["rolling_avg"] = group_df["total_updates"].rolling(3).mean()
        group_df["trend_deviation"] = (
            group_df["total_updates"] - group_df["rolling_avg"]
        )

        group_df.fillna(0, inplace=True)

        # ML features
        features = [
            "total_updates",
            "update_growth_rate",
            "trend_deviation"
        ]

        X = group_df[features]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = IsolationForest(
            n_estimators=200,
            contamination=0.15,
            random_state=42
        )

        group_df["anomaly_flag"] = model.fit_predict(X_scaled)
        group_df["anomaly"] = group_df["anomaly_flag"].map(
            {1: "Normal", -1: "Anomaly"}
        )

        # =================================================
        # 8. Severity score & level
        # =================================================
        group_df["severity_score"] = (
            abs(group_df["update_growth_rate"]) * 100 +
            abs(group_df["trend_deviation"]) / 1_000_000
        )

        def severity_level(score):
            if score >= 70:
                return "High"
            elif score >= 30:
                return "Medium"
            else:
                return "Low"

        group_df["severity_level"] = group_df["severity_score"].apply(severity_level)

        # =================================================
        # 9. Anomaly type classification
        # =================================================
        def classify_anomaly(row):
            if row["update_growth_rate"] > 0.3:
                return "Sudden Spike in Updates"
            elif row["update_growth_rate"] < -0.3:
                return "Sudden Drop in Updates"
            elif abs(row["trend_deviation"]) > 2_000_000:
                return "Unusual Volume Deviation"
            else:
                return "Irregular Pattern"

        group_df["anomaly_type"] = group_df.apply(classify_anomaly, axis=1)

        # =================================================
        # 10. Recommended actions
        # =================================================
        def recommend_action(row):
            if row["anomaly_type"] == "Sudden Spike in Updates":
                return "Increase staff, check system load"
            elif row["anomaly_type"] == "Sudden Drop in Updates":
                return "Check connectivity and system uptime"
            elif row["anomaly_type"] == "Unusual Volume Deviation":
                return "Operational audit recommended"
            else:
                return "Monitor closely"

        group_df["recommended_action"] = group_df.apply(
            recommend_action, axis=1
        )

        results.append(group_df)

    # =====================================================
    # 11. Combine all groups
    # =====================================================
    final_df = pd.concat(results).reset_index(drop=True)

    return final_df
