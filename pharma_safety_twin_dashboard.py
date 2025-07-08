
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the simulated Odoo IoT log file
st.set_page_config(page_title="Odoo IoT - Safety Risk Dashboard", layout="wide")
st.title("📈 Pharma Safety Digital Twin - Weekly Risk Dashboard")

# Use a safe path to load the CSV
csv_path = os.path.join(os.path.dirname(__file__), "odoo_iot_log.csv")
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("CSV log file not found. Please upload or provide the correct path.")
    st.stop()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Display latest records
st.subheader("📄 Latest Safety Log")
st.dataframe(df.tail(7))

# Risk trends
st.subheader("📊 Risk Score Trends (Last 7 Days)")
fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax[0].plot(df["Date"], df["ContaminationRiskScore"], marker='o', color='green')
ax[0].set_ylabel("Contamination Risk")
ax[0].axhline(40, color='black', linestyle='--')
ax[0].axhline(70, color='black', linestyle='--')

ax[1].plot(df["Date"], df["FireRiskScore"], marker='s', color='orange')
ax[1].set_ylabel("Fire Risk")
ax[1].axhline(40, color='black', linestyle='--')
ax[1].axhline(70, color='black', linestyle='--')

ax[2].plot(df["Date"], df["EquipmentFailureRiskScore"], marker='^', color='red')
ax[2].set_ylabel("Equipment Risk")
ax[2].set_xlabel("Date")
ax[2].axhline(40, color='black', linestyle='--')
ax[2].axhline(70, color='black', linestyle='--')

plt.tight_layout()
st.pyplot(fig)

# Summary
st.subheader("📝 Weekly Risk Summary")
risk_summary = df[["ContaminationRiskScore", "FireRiskScore", "EquipmentFailureRiskScore"]].mean()
st.write("**Average Risk Scores:**")
st.write(risk_summary)

# High risk alerts
st.subheader("🚨 High Risk Alerts")
high_risk_days = df[(df["ContaminationRiskScore"] >= 70) |
                    (df["FireRiskScore"] >= 70) |
                    (df["EquipmentFailureRiskScore"] >= 70)]
if not high_risk_days.empty:
    st.dataframe(high_risk_days[["Date", "ContaminationRiskScore", "FireRiskScore", "EquipmentFailureRiskScore"]])
else:
    st.success("No HIGH risk days recorded in the past week.")
