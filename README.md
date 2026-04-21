ConversionRateCHAOSS

A contributor conversion analytics system inspired by CHAOSS metrics. It analyzes GitHub repository activity to quantify how effectively first-time contributors transition into recurring and sustained contributors within open-source projects.


What It Does

ConversionRateCHAOSS collects contributor activity data from the GitHub REST API including commits, pull requests, and issue interactions. It processes and structures contributor timelines to identify participation frequency and behavioral patterns over time. Based on configurable lifecycle thresholds, contributors are classified into defined stages (D0 → D1 → D2) to measure progression from initial contribution to sustained engagement. The system then computes conversion and retention metrics and presents these insights through an interactive dashboard enabling maintainers to visualize contributor trends, detect drop-off points and make data-driven community improvements.


Workflow

The system follows an asynchronous data pipeline architecture. The FastAPI backend handles incoming analysis requests and asynchronously fetches contributor data from the GitHub REST API. Retrieved data is processed using Pandas to construct contributor timelines and compute lifecycle transitions (D0 → D1 → D2). The computed metrics are returned as structured JSON responses which are consumed by the React frontend for real-time visualization through interactive charts.


Conversion Stages

D0 — First 20 contribution

D1 — more than 20 contributions 

D2 — more than threshold value contributions

Conversion Rate = (D1 or D2 contributors / D0 contributors) × 100


Tech Stack

Python (FastAPI)

Pandas

React

GitHub REST API


Run Locally
Backend:
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:
```
cd frontend
npm install
npm run dev
```
