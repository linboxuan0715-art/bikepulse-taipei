# BikePulse Taipei: Real-time YouBike Supply-Demand Dashboard

## Live Dashboard URL

https://bikepulse-taipei-n7jxuvpveahv69pylhqtnk.streamlit.app

## GitHub Repository

https://github.com/linboxuan0715-art/bikepulse-taipei

## 1. Project Overview

BikePulse Taipei is a real-time dashboard designed to monitor YouBike station availability across Taipei. The project uses Taipei YouBike 2.0 open data to analyze station-level supply and demand conditions, identify bike shortages, and detect docking shortages.

The goal of this project is to transform real-time transportation data into an interactive dashboard that helps users and operators quickly understand where bike-sharing imbalance occurs across the city.

## 2. Data Source

The dashboard uses Taipei YouBike 2.0 real-time open data in JSON format.

The dataset contains station-level information, including station name, district, address, total parking slots, available bikes, available docks, latitude, longitude, and data update time.

## 3. Data Pipeline

The project follows an ETL data pipeline.

### Extract

The system fetches real-time station-level data from the public YouBike API using Python `requests`.

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

Compares YouBike supply-demand conditions across Taipei districts using bar charts and a scatter plot.

### Problem Stations

Ranks stations with the lowest bike availability and lowest dock availability, helping identify locations that may require bike redistribution or docking-space relief.

### Map

Displays all YouBike stations on an interactive map, allowing users to inspect real-time station availability by location.

## 5. Data Refresh Mechanism

The dashboard uses Streamlit cache with a 5-minute time-to-live setting:

```python
@st.cache_data(ttl=300)
```

This allows the dashboard to automatically refresh real-time data every five minutes. A manual refresh button is also provided in the sidebar.

## 6. Key Insights

This dashboard highlights two different types of operational imbalance in the YouBike system:

1. Low bike availability means users may have difficulty renting bikes.
2. Low dock availability means users may have difficulty returning bikes.

By separating these two indicators, the dashboard provides a clearer view of supply-demand imbalance and can support better real-time bike redistribution decisions.

## 7. Tools Used

- Python
- Streamlit
- pandas
- requests
- Plotly

## 8. Project Value

BikePulse Taipei demonstrates how public open data can be transformed into a practical decision-support dashboard. Instead of only showing raw station-level data, the project turns real-time information into actionable indicators for users, city operators, and transportation planners.