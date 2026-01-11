Aadhaar Anomaly Detection System

This project analyzes Aadhaar enrolment and update data to detect unusual patterns such as sudden spikes, abnormal volume deviations, and irregular trends. These anomalies may indicate operational issues or system inefficiencies. The system uses machine learning to identify anomalies and presents insights through an API and an interactive dashboard.

Objectives:

Detect anomalies in Aadhaar enrolment and update data

Classify anomalies by severity level

Provide actionable insights for monitoring

Visualize results through a dashboard

Enable automated monthly anomaly checks


Key Features:

Machine learning–based anomaly detection (Isolation Forest)

Severity scoring and classification

FastAPI backend for data processing

Streamlit dashboard for visualization

Automated monthly monitoring


Project Structure
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


Dataset:

Aadhaar enrolment and update data

Source: UIDAI Open Government Data Platform

Format: CSV (aggregated monthly data)

Technology Stack:

Python

Scikit-learn

FastAPI

Streamlit

Pandas, NumPy

How to Run:

Start Backend

cd backend

uvicorn main:app --reload

Start Dashboard

cd dashboard

streamlit run app.py


Output:

Anomaly detection results in CSV format

Interactive dashboard for monitoring

Since the project involves unsupervised anomaly detection and no labeled ground truth is available, traditional accuracy metrics are not applicable. The model is evaluated using severity scoring, anomaly rate analysis, and temporal pattern validation.

Disclaimer:
This project uses publicly available aggregated data and is intended for academic and analytical purposes only.

Author:

Chinmayee Reddy
