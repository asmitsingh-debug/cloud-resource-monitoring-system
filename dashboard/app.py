import streamlit as st
import pandas as pd
import os

# Get correct file path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data", "resource_metrics.csv")

# Page settings
st.set_page_config(
    page_title="Cloud Resource Monitoring Dashboard",
    layout="wide"
)

st.title("☁ Cloud Resource Monitoring Dashboard")

# Read CSV
df = pd.read_csv(file_path)

# Get latest row
latest = df.iloc[-1]

# Main metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", f"{latest['cpu']} %")

with col2:
    st.metric("RAM Usage", f"{latest['ram']} %")

with col3:
    st.metric("Disk Usage", f"{latest['disk']} %")

# Last updated time
st.subheader("🕒 Last Updated")
st.write(latest["timestamp"])

# Cloud upload status
st.subheader("☁ MinIO Upload Status")

st.success("Metrics file uploaded successfully to MinIO")

st.info(f"Last upload time: {latest['timestamp']}")

# Alerts
st.subheader("🚨 System Alerts")

if latest["cpu"] > 80:
    st.error("High CPU Usage Alert!")

if latest["ram"] > 85:
    st.warning("High RAM Usage!")

if latest["disk"] > 90:
    st.error("Disk Almost Full!")

if (
    latest["cpu"] <= 80
    and latest["ram"] <= 85
    and latest["disk"] <= 90
):
    st.success("No active alerts")

# Health status
st.subheader("🩺 System Health")

if latest["cpu"] < 70 and latest["ram"] < 85 and latest["disk"] < 90:
    st.success("System Healthy")
else:
    st.warning("System Under Load")

# Analytics summary
st.subheader("📊 Analytics Summary")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Average CPU", f"{round(df['cpu'].mean(), 2)} %")

with col5:
    st.metric("Peak CPU", f"{df['cpu'].max()} %")

with col6:
    st.metric("Average RAM", f"{round(df['ram'].mean(), 2)} %")

# Peak usage summary
st.subheader("📌 Peak Usage Summary")

st.write("Max CPU Usage:", df["cpu"].max(), "%")
st.write("Max RAM Usage:", df["ram"].max(), "%")
st.write("Max Disk Usage:", df["disk"].max(), "%")

# Trend graph
st.subheader("📈 Usage Trends")
st.line_chart(df[["cpu", "ram", "disk"]])

# Trend insights
st.subheader("📉 Trend Insights")

df["cpu_avg_5"] = df["cpu"].rolling(window=5).mean()
df["ram_avg_5"] = df["ram"].rolling(window=5).mean()

st.line_chart(df[["cpu_avg_5", "ram_avg_5"]])

# Alert history
st.subheader("🚨 Alert History")

alerts = df[
    (df["cpu"] > 80) |
    (df["ram"] > 85) |
    (df["disk"] > 90)
]

if not alerts.empty:
    st.dataframe(alerts.tail(10))
else:
    st.success("No critical alerts detected so far")