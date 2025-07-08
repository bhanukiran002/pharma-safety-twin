
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import base64
import os

st.set_page_config(page_title="Pharma Twin Playback", layout="wide")
st.title("📽️ Pharma Safety Twin Playback – 5-Min Simulation with Siren")

# Load new 5-min dataset
df = pd.read_csv("pharma_iot_simulated_5min.csv", parse_dates=["Timestamp"])

# Sidebar controls
st.sidebar.header("🎛 Playback Controls")
play = st.sidebar.button("▶ Start Playback")
speed = st.sidebar.slider("⏱ Seconds per step", 1, 10, 3)

# Equipment coordinates and color mapping
color_map = {"Normal": "green", "Warning": "orange", "High Risk": "red"}
equipment = df["Equipment"].unique().tolist()
coords = {eq: (x, y, 0) for eq, (x, y) in zip(equipment, [(2,8),(5,7),(8,6),(3,3),(6,3),(9,2)])}
time_steps = sorted(df["Timestamp"].unique())

# Layout placeholders
plot_area = st.empty()
audio_area = st.empty()
table_area = st.empty()

# Load and encode the siren audio
def get_audio_html():
    file_path = "siren_alert.mp3"
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'''
    <audio autoplay loop>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    '''

# Playback loop
if play:
    for ts in time_steps:
        snapshot = df[df["Timestamp"] == ts]
        colors = [color_map[s] for s in snapshot["Status"]]

        fig = go.Figure(data=[go.Scatter3d(
            x=[coords[eq][0] for eq in snapshot["Equipment"]],
            y=[coords[eq][1] for eq in snapshot["Equipment"]],
            z=[coords[eq][2] for eq in snapshot["Equipment"]],
            mode='markers+text',
            marker=dict(size=18, color=colors, opacity=0.85),
            text=snapshot["Equipment"],
            textposition="top center"
        )])

        fig.update_layout(
            title=f"🕒 Time: {ts}",
            scene=dict(aspectmode="data"),
            margin=dict(t=40, b=0)
        )

        plot_area.plotly_chart(fig, use_container_width=True)
        table_area.subheader(f"📋 Equipment Status at {ts}")
        table_area.dataframe(snapshot)

        if "Warning" in snapshot["Status"].values:
            audio_area.markdown(get_audio_html(), unsafe_allow_html=True)
        else:
            audio_area.empty()

        time.sleep(speed)
