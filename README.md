# BikePulse Taipei 🚲

## Live Demo

https://bikepulse-taipei-n7jxuvpveahv69pylhqtnk.streamlit.app

## Real-time YouBike Supply-Demand Dashboard

BikePulse Taipei is a real-time dashboard that monitors YouBike station availability across Taipei.  
The dashboard uses public YouBike open data to identify bike shortages, docking shortages, and district-level supply-demand imbalance.

## Project Motivation

Urban bike-sharing systems often face real-time supply-demand imbalance. Some stations may run out of bikes, while others may have no empty docks for bike return.

This project transforms station-level open data into an interactive dashboard that helps users and operators quickly understand where imbalance occurs.

## Data Source

- Source: Taipei YouBike 2.0 Open Data
- Format: JSON API
- Data fields include:
  - Station name
  - District
  - Address
  - Total slots
  - Available bikes
  - Available docks
  - Latitude and longitude
  - Update time

## Data Pipeline

The data pipeline follows an ETL structure.

### 1. Extract

The dashboard fetches real-time YouBike station data from the public API using Python `requests`.

### 2. Transform

The raw JSON data is converted into a structured pandas DataFrame.  
The transformation process includes:

- Standardizing column names
- Converting numeric fields
- Removing inactive or invalid stations
- Calculating bike availability rate
- Calculating dock availability rate
- Identifying low-bike stations
- Identifying docking-shortage stations

### 3. Load

The processed data is loaded into a Streamlit dashboard and visualized through KPI cards, charts, ranking tables, and a station map.

## Dashboard Features

The dashboard contains four main sections.

### 1. Overview

Shows key system-level indicators, including:

- Active stations
- Available bikes
- Available docks
- Total capacity
- Average bike availability rate
- Average dock availability rate
- Number of low-bike stations
- Number of docking-shortage stations

### 2. District Comparison

Compares YouBike supply-demand conditions across Taipei districts using bar charts and a scatter plot.

This section helps identify which districts have relatively lower bike availability or lower dock availability.

### 3. Problem Stations

Ranks stations with potential bike shortages and docking shortages.

- Low-bike stations indicate locations where users may not be able to rent a bike.
- Docking-shortage stations indicate locations where users may not be able to return a bike.

### 4. Map

Displays station-level availability on an interactive map.

Users can inspect each station by location and view information such as district, available bikes, available docks, total slots, and bike availability rate.

## Data Refresh Mechanism

The dashboard uses Streamlit cache with a 5-minute TTL setting.

```python
@st.cache_data(ttl=300)
```

This means the dashboard automatically refreshes the data every 5 minutes.  
Users can also manually refresh the data through the sidebar button.

## Tech Stack

- Python
- Streamlit
- pandas
- requests
- Plotly

## How to Run Locally

Install required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## Project Structure

```text
bikepulse-taipei/
├── app.py
├── requirements.txt
├── README.md
└── executive_summary.md
```

## Key Insight

This dashboard shows that YouBike imbalance should be understood from two different perspectives:

1. Low bike availability means users may not be able to rent a bike.
2. Low dock availability means users may not be able to return a bike.

By separating these two indicators, the dashboard can better support real-time rebalancing decisions.

## Repository

https://github.com/linboxuan0715-art/bikepulse-taipei