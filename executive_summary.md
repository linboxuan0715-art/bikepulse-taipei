# BikePulse Taipei: Real-time YouBike Supply-Demand Dashboard

## 1. Project Overview

BikePulse Taipei is a real-time dashboard designed to monitor YouBike station availability across Taipei. The project uses public YouBike open data to analyze station-level supply and demand conditions, identify bike shortages, and detect docking shortages.

The goal of this project is to transform real-time transportation data into an interactive dashboard that supports quick understanding of urban bike-sharing imbalance.

## 2. Data Source

The dashboard uses Taipei YouBike 2.0 real-time open data in JSON format.

The dataset contains station-level information, including:

- Station name
- District
- Address
- Total parking slots
- Available bikes
- Available docks
- Latitude and longitude
- Data update time

## 3. Data Pipeline

The project follows an ETL data pipeline:

### Extract

The system fetches real-time station data from the public YouBike API using Python `requests`.

### Transform

The raw JSON data is transformed with `pandas`. The transformation process includes:

- Standardizing column names
- Converting numeric fields
- Removing inactive or invalid stations
- Calculating bike availability rate
- Calculating dock availability rate
- Identifying low-bike stations
- Identifying docking-shortage stations

### Load

The cleaned data is loaded into a Streamlit dashboard and visualized through KPI cards, district-level charts, ranking tables, and an interactive map.

## 4. Dashboard Design

The dashboard contains four main sections:

### Overview

Shows system-level KPIs such as active stations, available bikes, available docks, total capacity, average bike availability, and average dock availability.

### District Comparison

Compares YouBike supply-demand conditions across Taipei districts using bar charts and scatter plots.

### Problem Stations

Ranks stations with the lowest bike availability and lowest dock availability, helping identify locations that may require rebalancing.

### Map

Displays all YouBike stations on an interactive map, allowing users to inspect real-time station availability by location.

## 5. Data Refresh Mechanism

The dashboard uses Streamlit cache with a 5-minute time-to-live setting:

```python
@st.cache_data(ttl=300)