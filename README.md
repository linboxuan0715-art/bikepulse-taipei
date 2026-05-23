## Live Demo

https://bikepulse-taipei-n7jxuvpveahv69pylhqtnk.streamlit.app

# BikePulse Taipei 🚲

## Real-time YouBike Supply-Demand Dashboard

BikePulse Taipei is a real-time dashboard that monitors YouBike station availability across Taipei.  
The dashboard uses public YouBike open data to identify bike shortages, docking shortages, and district-level supply-demand imbalance.

## Project Motivation

Urban bike-sharing systems often face real-time supply-demand imbalance.  
Some stations may run out of bikes, while others may have no empty docks for bike return.  
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

The data pipeline follows an ETL structure:

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

The dashboard contains four main sections:

### 1. Overview

Shows key system-level indicators, including total active stations, available bikes, available docks, and average availability rates.

### 2. District Comparison

Compares YouBike supply-demand conditions across districts using bar charts and scatter plots.

### 3. Problem Stations

Ranks stations with potential bike shortages and docking shortages.

### 4. Map

Displays station-level availability on an interactive map.

## Data Refresh Mechanism

The dashboard uses Streamlit cache with a 5-minute TTL setting.

```python
@st.cache_data(ttl=300)