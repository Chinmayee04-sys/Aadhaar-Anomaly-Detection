import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------------------------------
# Page configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Aadhaar Anomaly Monitoring Dashboard",
    layout="wide"
)

st.title("Aadhaar Anomaly Monitoring Dashboard")

# ----------------------------------------------------
# Load data
# ----------------------------------------------------
DATA_PATH = Path("../backend/outputs/aadhaar_anomaly_report.csv")

if not DATA_PATH.exists():
    st.error("Anomaly report not found. Please run the backend first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# Convert month column safely
if "month" in df.columns:
    df["month"] = pd.to_datetime(df["month"], errors="coerce")

# ----------------------------------------------------
# KPI Section
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric(
    "Total Anomalies",
    df[df.get("anomaly", "") == "Anomaly"].shape[0]
)

if "severity_level" in df.columns:
    col3.metric(
        "High Severity Alerts",
        df[df["severity_level"] == "High"].shape[0]
    )
else:
    col3.metric("High Severity Alerts", "N/A")

st.divider()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.header("Filters")

filtered_df = df.copy()

# Severity filter
if "severity_level" in df.columns:
    severity_filter = st.sidebar.multiselect(
        "Severity Level",
        options=sorted(df["severity_level"].unique()),
        default=sorted(df["severity_level"].unique())
    )
    filtered_df = filtered_df[
        filtered_df["severity_level"].isin(severity_filter)
    ]

# State filter (optional)
if "state" in df.columns:
    state_filter = st.sidebar.multiselect(
        "State",
        options=sorted(df["state"].dropna().unique()),
        default=sorted(df["state"].dropna().unique())
    )
    filtered_df = filtered_df[
        filtered_df["state"].isin(state_filter)
    ]

# ----------------------------------------------------
# Severity color function
# ----------------------------------------------------
def highlight_severity(val):
    if val == "High":
        return "background-color: #ff4d4d; color: white;"   # 🔴 Red
    elif val == "Medium":
        return "background-color: #ffa500; color: black;"  # 🟠 Orange
    elif val == "Low":
        return "background-color: #4CAF50; color: white;"  # 🟢 Green
    return ""

# ----------------------------------------------------
# Detected Anomalies Table
# ----------------------------------------------------
st.subheader("Detected Anomalies")

st.markdown(
    "**Severity Legend:** 🟢 Low &nbsp;&nbsp; 🟠 Medium &nbsp;&nbsp; 🔴 High"
)

preferred_columns = [
    "month",
    "state",
    "district",
    "total_updates",
    "anomaly_type",
    "severity_level",
    "severity_score",
    "recommended_action"
]

available_columns = [
    col for col in preferred_columns if col in filtered_df.columns
]

if not available_columns:
    st.warning("No displayable columns found in the dataset.")
else:
    display_df = filtered_df[available_columns]

    if "severity_level" in display_df.columns:
        display_df = display_df.style.applymap(
            highlight_severity,
            subset=["severity_level"]
        )

    st.dataframe(
        display_df,
        use_container_width=True
    )

# ----------------------------------------------------
# Trend Chart
# ----------------------------------------------------
st.subheader("Monthly Update Trend")

if "month" in filtered_df.columns and "total_updates" in filtered_df.columns:
    trend_df = filtered_df.sort_values("month")
    st.line_chart(
        trend_df.set_index("month")["total_updates"]
    )
else:
    st.info("Trend chart not available for this dataset.")

# ----------------------------------------------------
# Download Section
# ----------------------------------------------------
st.subheader("Download")

st.download_button(
    label="Download Filtered Anomaly Report (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="aadhaar_anomaly_report_filtered.csv",
    mime="text/csv"
)

# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.caption(
    "Aadhaar Anomaly Detection Dashboard | "
    "Severity-aware monitoring of enrolment and update patterns"
)
