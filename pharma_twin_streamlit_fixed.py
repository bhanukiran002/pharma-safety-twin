
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime

st.set_page_config(page_title="Pharma Safety Twin", layout="wide")

st.title("🧪 Pharma Safety Digital Twin - Real-Time Monitoring")
st.sidebar.header("🔄 Live Monitoring Settings")
auto_refresh = st.sidebar.checkbox("Enable Live Refresh (every 5s)", value=True)
refresh_now = st.sidebar.button("🔃 Refresh Now")

# Inject HTML meta refresh tag for 5s refresh
if auto_refresh:
    st.markdown("<meta http-equiv='refresh' content='5'>", unsafe_allow_html=True)

# Equipment and thresholds
equipment_list = [
    "Reactor 1", "Solvent Tank A", "Centrifuge 1", 
    "Compressor", "Boiler", "Mixing Kettle"
]

thresholds = {
    "Reactor 1": {"pressure": 3.0, "temperature": 200},
    "Solvent Tank A": {"voc": 50},
    "Centrifuge 1": {"rpm": 3000},
    "Compressor": {"pressure": 6.0},
    "Boiler": {"temperature": 180, "pressure": 2.0},
    "Mixing Kettle": {"rpm": 1500, "temperature": 90}
}

def simulate_iot_data():
    records = []
    timestamp = datetime.now()
    for eq in equipment_list:
        data = {"Timestamp": timestamp, "Equipment": eq}
        if "pressure" in thresholds[eq]:
            data["Pressure"] = round(random.uniform(1.0, 4.5), 2)
        if "temperature" in thresholds[eq]:
            data["Temperature"] = round(random.uniform(60, 250), 1)
        if "rpm" in thresholds[eq]:
            data["RPM"] = random.randint(1000, 3500)
        if "voc" in thresholds[eq]:
            data["VOC"] = random.randint(10, 100)
        records.append(data)
    return pd.DataFrame(records)

def evaluate_status(row):
    eq = row["Equipment"]
    if eq == "Reactor 1":
        if row.get("Pressure", 0) > thresholds[eq]["pressure"] or row.get("Temperature", 0) > thresholds[eq]["temperature"]:
            return "High Risk"
    elif eq == "Solvent Tank A":
        if row.get("VOC", 0) > thresholds[eq]["voc"]:
            return "High Risk"
    elif eq == "Centrifuge 1":
        if row.get("RPM", 0) > thresholds[eq]["rpm"]:
            return "High Risk"
    elif eq == "Compressor":
        if row.get("Pressure", 0) > thresholds[eq]["pressure"]:
            return "High Risk"
    elif eq == "Boiler":
        if row.get("Pressure", 0) > thresholds[eq]["pressure"] or row.get("Temperature", 0) > thresholds[eq]["temperature"]:
            return "High Risk"
    elif eq == "Mixing Kettle":
        if row.get("RPM", 0) > thresholds[eq]["rpm"] or row.get("Temperature", 0) > thresholds[eq]["temperature"]:
            return "High Risk"
    return "Normal"

# Generate data and evaluate
df = simulate_iot_data()
df["Status"] = df.apply(evaluate_status, axis=1)

# Coordinates for 3D layout
x_coords = [2, 5, 8, 3, 6, 9]
y_coords = [8, 7, 6, 3, 3, 2]
z_coords = [0, 0, 0, 0, 0, 0]
color_map = {"Normal": "green", "High Risk": "red"}
colors = [color_map[status] for status in df["Status"]]

# 3D Plot
fig = go.Figure(data=[
    go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode='markers+text',
        marker=dict(size=18, color=colors, opacity=0.85),
        text=df["Equipment"].tolist(),
        textposition="top center"
    )
])

fig.update_layout(
    title="3D Plant Layout - Equipment Status",
    scene=dict(
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        zaxis_title="Height",
        aspectratio=dict(x=1, y=1, z=0.3),
        camera=dict(eye=dict(x=1.6, y=1.6, z=0.6))
    ),
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# Live Alert Table
st.subheader("🚨 Live Equipment Status")
st.dataframe(df)
