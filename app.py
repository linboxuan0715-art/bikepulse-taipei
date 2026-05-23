import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# =========================
# Basic Page Settings
# =========================

st.set_page_config(
    page_title="BikePulse Taipei",
    page_icon="🚲",
    layout="wide"
)

DATA_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"


# =========================
# Data Pipeline: Extract + Transform
# =========================

def pick_column(df, candidates):
    """Return the first available column name from candidates."""
    for col in candidates:
        if col in df.columns:
            return col
    return None


@st.cache_data(ttl=300)
def load_youbike_data():
    """
    Extract:
        Fetch real-time YouBike station data from Taipei open data API.

    Transform:
        Standardize column names, convert numeric fields, and create useful indicators.
    """

    response = requests.get(DATA_URL, timeout=10)
    response.raise_for_status()
    raw_data = response.json()

    df = pd.DataFrame(raw_data)

    station_col = pick_column(df, ["sna"])
    district_col = pick_column(df, ["sarea"])
    address_col = pick_column(df, ["ar"])
    total_col = pick_column(df, ["tot", "Quantity"])
    bike_col = pick_column(df, ["sbi", "available_rent_bikes"])
    dock_col = pick_column(df, ["bemp", "available_return_bikes"])
    lat_col = pick_column(df, ["lat", "latitude"])
    lng_col = pick_column(df, ["lng", "longitude"])
    update_col = pick_column(df, ["updateTime", "mday", "infoTime"])
    active_col = pick_column(df, ["act"])

    clean = pd.DataFrame({
        "station_name": df[station_col],
        "district": df[district_col],
        "address": df[address_col],
        "total_slots": pd.to_numeric(df[total_col], errors="coerce"),
        "available_bikes": pd.to_numeric(df[bike_col], errors="coerce"),
        "available_docks": pd.to_numeric(df[dock_col], errors="coerce"),
        "lat": pd.to_numeric(df[lat_col], errors="coerce"),
        "lng": pd.to_numeric(df[lng_col], errors="coerce"),
        "update_time": df[update_col],
    })

    if active_col is not None:
        clean["active"] = df[active_col].astype(str)
        clean = clean[clean["active"].isin(["1", "True", "true"])]

    clean["station_name"] = clean["station_name"].astype(str).str.replace("YouBike2.0_", "", regex=False)

    clean = clean.dropna(subset=["total_slots", "available_bikes", "available_docks", "lat", "lng"])

    clean["bike_availability_rate"] = clean["available_bikes"] / clean["total_slots"]
    clean["dock_availability_rate"] = clean["available_docks"] / clean["total_slots"]

    clean["bike_availability_rate"] = clean["bike_availability_rate"].fillna(0)
    clean["dock_availability_rate"] = clean["dock_availability_rate"].fillna(0)

    clean["low_bike_station"] = clean["bike_availability_rate"] <= 0.15
    clean["docking_shortage_station"] = clean["dock_availability_rate"] <= 0.15

    return clean


try:
    df = load_youbike_data()
except Exception as e:
    st.error("資料讀取失敗，請稍後再試。")
    st.exception(e)
    st.stop()


# =========================
# Sidebar
# =========================

st.sidebar.title("🚲 BikePulse Taipei")
st.sidebar.caption("Real-time YouBike Supply-Demand Dashboard")

district_options = sorted(df["district"].dropna().unique())
selected_districts = st.sidebar.multiselect(
    "選擇行政區",
    options=district_options,
    default=district_options
)

if st.sidebar.button("手動重新整理資料"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("資料來源：臺北市 YouBike2.0 即時公開資料")
st.sidebar.write("自動更新：每 5 分鐘重新抓取一次資料")

filtered_df = df[df["district"].isin(selected_districts)].copy()


# =========================
# Header
# =========================

st.title("BikePulse Taipei 🚲")
st.subheader("Real-time YouBike Supply-Demand Dashboard")

latest_time = filtered_df["update_time"].max()

st.caption(
    f"Last updated: {latest_time} | "
    "This dashboard monitors real-time YouBike station availability across Taipei."
)


# =========================
# KPI Cards
# =========================

total_stations = len(filtered_df)
total_slots = int(filtered_df["total_slots"].sum())
total_bikes = int(filtered_df["available_bikes"].sum())
total_docks = int(filtered_df["available_docks"].sum())
avg_bike_rate = filtered_df["bike_availability_rate"].mean()
avg_dock_rate = filtered_df["dock_availability_rate"].mean()
low_bike_count = int(filtered_df["low_bike_station"].sum())
docking_shortage_count = int(filtered_df["docking_shortage_station"].sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Stations", f"{total_stations:,}")
col2.metric("Available Bikes", f"{total_bikes:,}")
col3.metric("Available Docks", f"{total_docks:,}")
col4.metric("Total Capacity", f"{total_slots:,}")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Avg. Bike Availability", f"{avg_bike_rate:.1%}")
col6.metric("Avg. Dock Availability", f"{avg_dock_rate:.1%}")
col7.metric("Low-bike Stations", f"{low_bike_count:,}")
col8.metric("Docking-shortage Stations", f"{docking_shortage_count:,}")


# =========================
# District Summary
# =========================

district_summary = (
    filtered_df
    .groupby("district", as_index=False)
    .agg(
        station_count=("station_name", "count"),
        total_slots=("total_slots", "sum"),
        available_bikes=("available_bikes", "sum"),
        available_docks=("available_docks", "sum"),
        avg_bike_availability=("bike_availability_rate", "mean"),
        avg_dock_availability=("dock_availability_rate", "mean"),
        low_bike_stations=("low_bike_station", "sum"),
        docking_shortage_stations=("docking_shortage_station", "sum"),
    )
)

district_summary["avg_bike_availability"] = district_summary["avg_bike_availability"].fillna(0)
district_summary["avg_dock_availability"] = district_summary["avg_dock_availability"].fillna(0)


# =========================
# Tabs
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "District Comparison",
    "Problem Stations",
    "Map"
])


with tab1:
    st.markdown("## Dashboard Overview")

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            district_summary.sort_values("avg_bike_availability", ascending=True),
            x="district",
            y="avg_bike_availability",
            title="Average Bike Availability Rate by District",
            labels={
                "district": "District",
                "avg_bike_availability": "Average Bike Availability Rate"
            },
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            district_summary.sort_values("avg_dock_availability", ascending=True),
            x="district",
            y="avg_dock_availability",
            title="Average Dock Availability Rate by District",
            labels={
                "district": "District",
                "avg_dock_availability": "Average Dock Availability Rate"
            },
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Interpretation")
    st.write(
        "A district with a low bike availability rate may indicate bike shortage, "
        "while a district with a low dock availability rate may indicate docking shortage. "
        "These two indicators help identify different types of supply-demand imbalance."
    )


with tab2:
    st.markdown("## District-level Supply-Demand Comparison")

    fig = px.scatter(
        district_summary,
        x="avg_bike_availability",
        y="avg_dock_availability",
        size="station_count",
        hover_name="district",
        title="District Supply-Demand Balance",
        labels={
            "avg_bike_availability": "Average Bike Availability Rate",
            "avg_dock_availability": "Average Dock Availability Rate",
            "station_count": "Station Count"
        },
    )
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        district_summary.sort_values("station_count", ascending=False),
        use_container_width=True
    )


with tab3:
    st.markdown("## Problem Station Ranking")

    left, right = st.columns(2)

    with left:
        st.markdown("### Top 10 Low-bike Stations")
        low_bike_table = (
            filtered_df
            .sort_values(["bike_availability_rate", "available_bikes"], ascending=[True, True])
            .head(10)
            [[
                "district",
                "station_name",
                "available_bikes",
                "available_docks",
                "total_slots",
                "bike_availability_rate",
                "update_time"
            ]]
        )
        st.dataframe(low_bike_table, use_container_width=True)

    with right:
        st.markdown("### Top 10 Docking-shortage Stations")
        docking_shortage_table = (
            filtered_df
            .sort_values(["dock_availability_rate", "available_docks"], ascending=[True, True])
            .head(10)
            [[
                "district",
                "station_name",
                "available_bikes",
                "available_docks",
                "total_slots",
                "dock_availability_rate",
                "update_time"
            ]]
        )
        st.dataframe(docking_shortage_table, use_container_width=True)

    st.markdown("### Operational Meaning")
    st.write(
        "Low-bike stations are locations where users may not be able to rent a bike. "
        "Docking-shortage stations are locations where users may not be able to return a bike. "
        "These rankings can support real-time rebalancing decisions."
    )


with tab4:
    st.markdown("## Station Map")

    map_df = filtered_df.copy()
    map_df["hover_text"] = (
        map_df["station_name"]
        + "<br>District: " + map_df["district"]
        + "<br>Available Bikes: " + map_df["available_bikes"].astype(int).astype(str)
        + "<br>Available Docks: " + map_df["available_docks"].astype(int).astype(str)
        + "<br>Total Slots: " + map_df["total_slots"].astype(int).astype(str)
    )

    fig = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lng",
        size="total_slots",
        color="bike_availability_rate",
        hover_name="station_name",
        hover_data={
            "district": True,
            "available_bikes": True,
            "available_docks": True,
            "total_slots": True,
            "bike_availability_rate": ":.1%",
            "lat": False,
            "lng": False,
        },
        zoom=11,
        height=650,
        title="Real-time YouBike Station Availability Map",
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


# =========================
# Footer
# =========================

st.markdown("---")
st.caption(
    "BikePulse Taipei | Built with Python, Streamlit, pandas, Plotly, and Taipei YouBike Open Data."
)