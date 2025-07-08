import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Odoo IoT - Safety Risk Dashboard", layout="wide")
st.title("📈 Pharma Safety Digital Twin - Real-Time Risk Dashboard")
st.info("👈 Use the sidebar on the **left** to enable 🔄 Live Mode or click 🔃 Refresh Now to simulate data.")

# Define log file path
csv_path = os.path.join(os.path.dirname(__file__), "odoo_iot_log.csv")

# Sidebar controls
st.sidebar.header("🛠 Controls")
live_mode = st.sidebar.checkbox("🔄 Live Mode (auto-refresh every 5 sec)", value=False)
refresh_now = st.sidebar.button("🔃 Refresh Now")

# Enable auto-refresh if live_mode is on
if live_mode:
    st_autorefresh(interval=5000, key="auto_refresh")

# Function to simulate a new row of IoT data
def simulate_new_data():
    date = datetime.now()  # Use raw datetime object
    filters = [random.choice(["OK", "DEGRADED"]) for _ in range(3)]
    worker_entries = random.randint(30, 70)
    flammable_units = random.randint(10, 90)
    equipment_runtime = round(random.uniform(8, 20), 2)
    contamination_risk = filters.count("DEGRADED") * 20 + max(0, (worker_entries - 40) * 2)
    fire_risk = flammable_units * 0.6 + max(0, (worker_entries - 40) * 1.5)
    failure_risk = max(0, (equipment_runtime - 12) * 5)
    return {
        "Date": date,
        "Filter1": filters[0],
        "Filter2": filters[1],
        "Filter3": filters[2],
        "WorkerEntries": worker_entries,
        "FlammableUnits": flammable_units,
        "EquipmentRuntime": equipment_runtime,
        "ContaminationRiskScore": contamination_risk,
        "FireRiskScore": fire_risk,
        "EquipmentFailureRiskScore": failure_risk
    }

# Load existing or create new DataFrame
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=["Date", "Filter1", "Filter2", "Filter3", "WorkerEntries", "FlammableUnits", "EquipmentRuntime", "ContaminationRiskScore", "FireRiskScore", "EquipmentFailureRiskScore"])

# Append new row if refresh or live mode is enabled
if refresh_now or live_mode:
    new_row = simulate_new_data()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(csv_path, index=False)

# Convert Date column to datetime safely
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Show latest records
st.subheader("📄 Latest Safety Log")
st.dataframe(df.tail(10))

# Risk score trends
st.subheader("📊 Risk Score Trends (Last 10 Entries)")
fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax[0].plot(df["Date"].tail(10), df["ContaminationRiskScore"].tail(10), marker='o', color='green')
ax[0].set_ylabel("Contamination Risk")
ax[0].axhline(40, color='black', linestyle='--')
ax[0].axhline(70, color='black', linestyle='--')

ax[1].plot(df["Date"].tail(10), df["FireRiskScore"].tail(10), marker='s', color='orange')
ax[1].set_ylabel("Fire Risk")
ax[1].axhline(40, color='black', linestyle='--')
ax[1].axhline(70, color='black', linestyle='--')

ax[2].plot(df["Date"].tail(10), df["EquipmentFailureRiskScore"].tail(10), marker='^', color='red')
ax[2].set_ylabel("Equipment Risk")
ax[2].set_xlabel("Timestamp")
ax[2].axhline(40, color='black', linestyle='--')
ax[2].axhline(70, color='black', linestyle='--')

plt.tight_layout()
st.pyplot(fig)

# Risk Summary
st.subheader("📝 Average Risk Scores (Last 10 Entries)")
risk_summary = df.tail(10)[["ContaminationRiskScore", "FireRiskScore", "EquipmentFailureRiskScore"]].mean()
st.write(risk_summary)

# High Risk Alerts
st.subheader("🚨 High Risk Alerts (Last 10 Entries)")
high_risk = df.tail(10)[(df["ContaminationRiskScore"] >= 70) | (df["FireRiskScore"] >= 70) | (df["EquipmentFailureRiskScore"] >= 70)]
if not high_risk.empty:
    st.dataframe(high_risk[["Date", "ContaminationRiskScore", "FireRiskScore", "EquipmentFailureRiskScore"]])
else:
    st.success("No HIGH risk values in the latest readings.")
