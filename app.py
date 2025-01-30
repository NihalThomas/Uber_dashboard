import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\HP\PycharmProjects\uber_data\Data source\uber_data.csv", parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [df["tpep_pickup_datetime"].min(), df["tpep_pickup_datetime"].max()])
vendor = st.sidebar.selectbox("Select Vendor", df["VendorID"].unique())
payment = st.sidebar.multiselect("Payment Type", df["payment_type"].unique(), default=df["payment_type"].unique())

# Apply Filters
df_filtered = df[(df["tpep_pickup_datetime"].dt.date >= date_range[0]) & 
                 (df["tpep_pickup_datetime"].dt.date <= date_range[1]) & 
                 (df["VendorID"] == vendor) &
                 (df["payment_type"].isin(payment))]


st.title("Uber Dashboard")

col1, col2, col3 = st.columns(3)
# KPI Metrics
with col1:
    st.metric("Total Trips", len(df_filtered))
#st.metric("Total Trips", len(df_filtered))
with col2:
    st.metric("Average Distance", round(df_filtered["trip_distance"].mean(), 2))
#st.metric("Average Distance", round(df_filtered["trip_distance"].mean(), 2))
with col3:
    st.metric("Total Revenue", f"${df_filtered['total_amount'].sum():,.2f}")

# Visualizations
st.subheader("Pickup & Drop-off Map")
fig_map = px.scatter_mapbox(df_filtered, lat="pickup_latitude", lon="pickup_longitude",
                            hover_data=["tpep_pickup_datetime"], zoom=10, height=400)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map)

st.subheader("Trip Distance Distribution")
fig_dist = px.histogram(df_filtered, x="trip_distance", nbins=50, title="Trip Distance Histogram")
st.plotly_chart(fig_dist)

st.subheader("Revenue Trends")
fig_revenue = px.line(df_filtered, x="tpep_pickup_datetime", y="total_amount", title="Revenue Over Time")
st.plotly_chart(fig_revenue)

st.subheader("Payment Type Distribution")
fig_payment = px.pie(df_filtered, names="payment_type", title="Payment Type Breakdown")
st.plotly_chart(fig_payment)

st.subheader("Tip Analysis")
fig_tips = px.box(df_filtered, x="payment_type", y="tip_amount", title="Tip Amount by Payment Type")
st.plotly_chart(fig_tips)

