# 🌍 Earthquake Monitoring & Analytics Platform

A real-time, multi-layer earthquake analytics system for geospatial visualization, time-series analysis, statistical exploration, and unsupervised machine learning.

The system transforms raw seismic events into structured insights through an end-to-end pipeline including data ingestion, storage, processing, analytics, and interactive visualization.

---

## 🚀 Live Application

The dashboard is deployed and accessible online:
👉 **[Launch Earthquake Monitoring Dashboard](https://earthquake-monitoring-dashboard.streamlit.app/)**

---

## 🧭 Project Overview

This platform is an end-to-end earthquake analytics system that integrates:

* Real-time seismic event monitoring (USGS API)
* Geospatial mapping of global earthquakes
* Time-series analysis of seismic activity
* Statistical distribution analysis (magnitude & depth)
* Unsupervised clustering for spatial pattern discovery

It supports both operational monitoring and exploratory data analysis.

---

## 🏗️ System Architecture

This system follows a layered analytical approach:
```text
Raw seismic events
   │
   ▼
Structured data
   │
   ▼
Statistical insights
   │
   ▼
Machine learning patterns
```
It separates three analytical perspectives:

* What is happening (live monitoring & map)
* How it evolves (time-series analysis)
* What patterns exist (clustering & statistics)

---
## 🔄 Data Pipeline Architecture
```text
USGS API
   │
   ▼
ETL Pipeline (Backfill + Incremental)
   │
   ▼
SQLite Database (earthquake.db)
   │
   ├── Data Catalog (raw data)
   ├── Filter Engine (user queries)
   │
   ▼
Filtered Dataset
   │
   ├── Analytics Engine (stats, trends)
   ├── ML Clustering (DBSCAN / HDBSCAN)
   │
   ▼
Streamlit Dashboard Layer
   │
   ├── PyDeck Map (spatial view)
   ├── Charts (time-series & distributions)
   ├── Data Table (raw catalog)
   │
   ▼
Interactive Linked Visualization System
```
---
## ✨ Key Features

### 🌍 Geospatial Visualization
* Interactive earthquake map
* Magnitude-based encoding
* Global event coverage
### 📊 Time-Series Analytics
* Earthquake frequency trends
* Magnitude over time visualization
* Rolling average smoothing (7-day window)
### 📈 Statistical Insights
* Magnitude distribution analysis
* Depth distribution patterns
### 🧠 Machine Learning Integration
* DBSCAN clustering for spatial grouping
* HDBSCAN for density-based clustering
* Interactive parameter controls (epsilon, min samples, etc.)
### 🔴 Live Monitoring System
* Real-time earthquake feed
* Magnitude-based alerting (M ≥ 5 warnings)
* Event catalog view

---

## 🧰 Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Altair
* PyDeck
* Scikit-learn
* HDBSCAN
* SQLite
* Requests (USGS API)

---
## 🧹 Data Engineering Pipeline
* Ingests real-time earthquake data from USGS (GeoJSON)
* Cleans and validates seismic records 
* Normalizes timestamps for consistency 
* Prevents duplicates using database constraints 
* Supports incremental ingestion (watermark-based updates)
* Stores structured data in SQLite

---

## 🧠 Machine Learning Details

* Clustering uses only latitude & longitude
* Distance metric: Haversine (geospatial distance)
* Noise points labeled as -1
* Magnitude & depth used only for visualization

### Controls
* Switch between DBSCAN and HDBSCAN 
* Tune parameters (eps, min_samples, cluster size)
* Toggle noise visibility

---
## 📁 Project Structure
```text
StreamlitEarthquakeDashboard/
├── assets/                 # dashboard screenshots
├── components/             # Streamlit UI components
├── data/                   # SQLite database
├── modules/                # data processing & feature engineering
├── scripts/                # batch jobs (backfill)
├── src/                    # ETL + database layer
│   ├── archived/
│   ├── db/
│   └── etl/
├── app.py                  # main Streamlit app
├── requirements.txt
└── README.md
```

---
## 📊 Design Philosophy

This system follows a layered analytical approach:

```text
Raw seismic events
   │
   ▼
Structured data
   │
   ▼
Statistical insights
   │
   ▼
Machine learning patterns
```
It separates three analytical perspectives:

* What is happening (live feed, map)
* How it evolves (time-series analysis)
* What patterns exist (clustering & statistics)

---

## 📸 Screenshots

### 🌍 Earthquake Map

Show spatial distribution of seismic events
![Map & KPIs](assets/map_tab.png)

### 📊 Time-Series Analysis

Frequency and magnitude trends over time
![Analytics](assets/analytics_tab.png)

### 🧠 Clustering Analysis

DBSCAN / HDBSCAN spatial grouping
![ML Clustering](assets/ml_tab.png)

### 🔴 Live Feed & Catalog

Real-time earthquake monitoring system
![Catalog](assets/catalog_tab.png)

---
## ▶️ How to Run Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Backfill (First-Time Setup)

```bash
python -m scripts.run_backfill
```

### 3. Start the Streamlit Application

```bash
streamlit run app.py
```

---

## 👤 Author

**Nurul Yakim Kazal**
Mathematics Department, Universitas Sam Ratulangi

Focus areas:
* Numerical Linear Algebra (academic)
* Data engineering & ETL systems
* Interactive analytics dashboards (Streamlit / Dash)
* Geospatial & time-series analytics

---
## 🚀 Final Note

This project demonstrates an end-to-end analytical system that integrates data engineering, real-time monitoring, statistical analysis, and machine learning into a unified interactive dashboard for exploring global earthquake activity.