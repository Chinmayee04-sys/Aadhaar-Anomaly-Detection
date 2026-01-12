# Aadhaar Anomaly Detection System

This project analyzes Aadhaar enrolment and update data to detect unusual patterns such as sudden spikes, abnormal volume deviations, and irregular trends that may indicate operational issues or system inefficiencies. It primarily uses the Aadhaar Demographic Update Dataset provided by UIDAI, which contains aggregated monthly update counts across regions. The dataset is well suited for identifying temporal anomalies without requiring labeled data. An unsupervised machine learning approach is applied to automatically detect abnormal patterns and assess their severity. The detected anomalies are presented through a FastAPI-based backend and an interactive dashboard to support effective monitoring and informed decision-making.

## Objectives:

- Detect anomalies in Aadhaar enrolment and update data
- Classify anomalies by severity level
- Provide actionable insights for monitorin
- Visualize results through a dashboard
- Enable automated monthly anomaly checks


## Key Features

- Machine learning–based anomaly detection using Isolation Forest
- Severity scoring and confidence-based prioritization
- Explainable anomaly detection with root cause hints
- Month-to-month change explanation for interpretability
- Early-warning forecasting for proactive monitoring
- FastAPI backend for data processing
- Streamlit dashboard for visualization
- Automated monthly anomaly monitoring


## Project Structure
Aadhaar_Anomaly_Detection/

├── backend/

│   ├── main.py

│   ├── model/anomaly_model.py

│   ├── data/

│   └── outputs/

├── dashboard/app.py

├── notebooks/

├── requirements.txt

└── README.md


## Dataset:
- Aadhaar Demographic Update Dataset provided by UIDAI
Source: UIDAI Open Government Data Platform

Format: CSV (aggregated monthly data)

## Technology Stack:
- Python
- Scikit-learn
- FastAPI
- Streamlit
- Pandas, NumPy

## How to Run:

Start Backend

cd backend

uvicorn main:app --reload

Start Dashboard

cd dashboard

streamlit run app.py


## Output

The system generates a structured anomaly analysis report after processing the uploaded Aadhaar update data.

## Backend API Output
The `/detect-anomalies` API returns a JSON response containing:
- Total number of records analyzed
- Total anomalies detected
- Detailed anomaly information for each affected month

Each anomaly record includes:
- Month
- Total update count
- Anomaly type (e.g., sudden spike, unusual deviation)
- Severity level (Low, Medium, High)
- Severity score
- Confidence score
- Explanation of why the anomaly was detected
- Month-to-month change description
- Root cause hint
- Early-warning forecast and alert message

## Sample API Response 

```json
{
  "total_records": 12,
  "anomalies_detected": 2,
  "results": [
    {
      "month": "2024-12-01",
      "total_updates": 26193030,
      "anomaly_type": "Sudden Spike in Updates",
      "severity_level": "Medium",
      "severity_score": 52.61,
      "confidence_score": 84.32,
      "what_changed": "Updates increased significantly compared to previous month",
      "root_cause_hint": "Seasonal demand surge or policy-driven update campaign",
      "early_warning_alert": "No early warning detected"
    }
  ]
}
Dashboard Output
- The Streamlit dashboard provides:
- Summary metrics (total records, anomalies, high-severity alerts)
- Tabular view of detected anomalies
- Severity-based visual indicators
- Clear explanations and recommended actions for monitoring

The dashboard enables quick interpretation of anomalies and supports informed operational and governance decisions.
## Model Evaluation
Since the project involves unsupervised anomaly detection and no labeled ground truth is available, traditional accuracy metrics are not applicable. The model is evaluated using severity scoring, anomaly rate analysis, and temporal pattern validation.


## Advanced Analytics and Governance Support
The system goes beyond basic anomaly detection by providing explainable and predictive insights. 
Each detected anomaly includes a root cause hint, a confidence score, and a clear explanation of what changed compared to the previous month. 
Additionally, an early-warning mechanism forecasts next-month update volumes and raises alerts when abnormal patterns are anticipated.
These features support proactive governance, operational planning, and service reliability monitoring.


## Disclaimer:
This project uses publicly available aggregated data and is intended for academic and analytical purposes only.

## Author:
- Chinmayee Reddy
