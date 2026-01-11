Aadhaar Anomaly Detection System

An end-to-end data analytics and machine learning system designed to detect unusual patterns in Aadhaar enrolment and update data, supporting improved monitoring, governance, and operational decision-making.

Problem Statement

Aadhaar enrolment and update centres occasionally exhibit unusual behaviour such as sudden spikes in update volumes, abnormal deviations, or irregular trends. These patterns may indicate operational inefficiencies, system issues, or potential misuse.

This project aims to analyze Aadhaar enrolment and update data to automatically identify such anomalies, evaluate their severity, and present actionable insights through an interactive dashboard and automated monitoring mechanisms.

Objectives

Detect anomalies in Aadhaar enrolment and update trends

Identify sudden spikes, drops, and unusual volume deviations

Assign severity levels (Low, Medium, High) to detected anomalies

Provide recommended operational actions

Visualize results using an interactive dashboard

Enable automated monthly anomaly monitoring

Key Features

Machine learning–based anomaly detection using Isolation Forest

Severity scoring and classification

State and district-level analysis (when data is available)

FastAPI backend for data ingestion and processing

Streamlit-based interactive dashboard

Automated monthly monitoring using APScheduler

CSV-based anomaly report generation

Project Architecture
Aadhaar_Anomaly_Detection/
│
├── backend/
│   ├── main.py               # FastAPI backend
│   ├── scheduler.py          # Automated monthly monitoring
│   ├── model/
│   │   └── anomaly_model.py  # Anomaly detection logic
│   ├── data/                 # Uploaded input data
│   └── outputs/              # Generated anomaly reports
│
├── dashboard/
│   └── app.py                # Streamlit dashboard
│
├── notebooks/                # Exploratory analysis (optional)
├── requirements.txt
├── README.md
└── .gitignore

Dataset

Aadhaar enrolment and update datasets

Source: UIDAI Open Government Data (OGD) Platform India

Format: CSV (monthly aggregated data)

Note: This project uses only publicly available, aggregated data and does not handle or store any personal Aadhaar information.

Technology Stack

Programming Language: Python

Machine Learning: Scikit-learn (Isolation Forest)

Backend Framework: FastAPI, Uvicorn

Dashboard Framework: Streamlit

Scheduler: APScheduler

Data Processing: Pandas, NumPy

How to Run the Project
Step 1: Install Dependencies
pip install -r requirements.txt

Step 2: Start Backend Service
cd backend
uvicorn main:app --reload


Backend URL:

http://127.0.0.1:8000


Swagger API Documentation:

http://127.0.0.1:8000/docs

Step 3: Upload Dataset and Detect Anomalies

Using the Swagger interface:

Call the POST /upload-data endpoint to upload the CSV file

Call the POST /detect-anomalies endpoint to run anomaly detection

This generates the anomaly report at:

backend/outputs/aadhaar_anomaly_report.csv

Step 4: Launch Dashboard

Open a new terminal and run:

cd dashboard
streamlit run app.py


Dashboard URL:

http://localhost:8501

Dashboard Capabilities

Display total records and detected anomalies

Filter anomalies by severity and region (if available)

Visualize monthly update trends

View severity-aware anomaly tables

Download filtered anomaly reports

Automated Monthly Monitoring

Monthly anomaly detection is automated using APScheduler

The scheduler starts automatically with the backend service

Default execution schedule is set to run once every month

Generates updated anomaly reports without manual intervention

Severity Classification
Severity Level	Description
Low	Minor variations requiring monitoring
Medium	Noticeable irregularities requiring operational review
High	Critical anomalies requiring immediate attention
Output

CSV anomaly reports containing:

Anomaly type

Severity score and level

Recommended operational actions

Interactive dashboard for monitoring and analysis

Disclaimer

This project is developed strictly for academic and analytical purposes. It does not integrate with or affect actual UIDAI systems or Aadhaar infrastructure.

Author

Chinmayee Reddy
B.Tech UnderGraduate
Machine Learning and Data Analytics Enthusiast
