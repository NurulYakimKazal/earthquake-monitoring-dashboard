# 🌍 Earthquake Monitoring & Analytics Platform

A multi-layer interactive dashboard for real-time earthquake monitoring, geospatial visualization, time-series analysis, and unsupervised machine learning clustering.

Built with Streamlit, this project transforms raw seismic event data into structured analytical insights through visualization, statistical exploration, and clustering-based pattern discovery.

---

## 🚀 Live Application

The dashboard is deployed and accessible online:
👉 **[Launch Earthquake Monitoring Dashboard](https://earthquake-monitoring-dashboard.streamlit.app/)**

---

## 🧭 Project Overview

This platform is designed as an end-to-end earthquake analytics system that integrates:

* Real-time seismic event monitoring
* Geospatial visualization of global earthquakes
* Time-series trend analysis and rolling statistics
* Statistical distribution analysis (magnitude & depth)
* Unsupervised machine learning for spatial clustering

It supports both operational monitoring (live activity) and exploratory data analysis (patterns & structure).

---

## 🏗️ System Architecture

The dashboard is structured into four analytical layers:
### 🌍 1. Observation Layer (What is happening?)
* Interactive global earthquake map
* Live earthquake activity feed
* Magnitude-based event highlighting
### 📊 2. Temporal Analysis Layer (How is it evolving?)
* Earthquake frequency over time
* Magnitude trends
* 7-day rolling average magnitude
### 📈 3. Statistical Analysis Layer (What are the characteristics?)
* Magnitude distribution
* Depth distribution
* Event-level exploration
### 🧠 4. Exploration Layer (What hidden structure exists?)
* DBSCAN clustering
* HDBSCAN clustering
* Interactive parameter tuning for spatial pattern discovery

### 🧠 Architecture Flow
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

## 🧠 Machine Learning Details

* Clustering uses only latitude & longitude
* Distance metric: Haversine (geospatial distance)
* Noise points labeled as -1
* Magnitude & depth used only for visualization

### Controls
* Switch between DBSCAN and HDBSCAN 
* Tune parameters (eps, min_samples, cluster size)
* Toggle noise visibility

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
* Requests

---
## 🧹 Data Pipeline
* Fetches earthquake data from USGS API (GeoJSON)
* Cleans missing/invalid magnitude values
* Normalizes timestamps
* Prevents duplicates using database constraints
* Uses incremental ingestion (watermark-based updates)
* Stores structured data in SQLite

---
## 🗄️ Database Schema

```sql
CREATE TABLE earthquakes (
    id TEXT PRIMARY KEY,
    magnitude REAL,
    place TEXT,
    time INTEGER,
    longitude REAL,
    latitude REAL,
    depth REAL
);
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

Data and analytics developer focused on building end-to-end analytical systems that combine data engineering, machine learning, and interactive visualization.

---
## 🚀 Final Note

This project demonstrates an end-to-end analytical system design, integrating data ingestion, storage, transformation, visualization, and machine learning into a single interactive platform for exploring global earthquake activity.