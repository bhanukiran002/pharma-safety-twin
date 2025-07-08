
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Pharma Twin Playback", layout="wide")
st.title("📽️ Pharma Safety Twin Playback - Risk Escalation Demo")

# Load the dataset
df = pd.read_csv("pharma_iot_time_series.csv", parse_dates=["Timestamp"])

# Sidebar settings
st.sidebar.header("🎛 Playback Controls")
play = st.sidebar.button("▶ Start Playback")
speed = st.sidebar.slider("⏱ Playback Speed (seconds per step)", 1, 10, 3)
auto_refresh = st.sidebar.checkbox("🔄 Auto-Refresh every 5s", value=False)

# Inject meta refresh only when enabled
if auto_refresh:
    refresh_code = "<meta http-equiv='refresh' content='5'>"
    st.markdown(refresh_code, unsafe_allow_html=True)
else:
    st.markdown("")  # Clear refresh when turned off

# Status color mapping
color_map = {"Normal": "green", "Warning": "orange", "High Risk": "red"}

# Coordinates for layout
equipment_list = df["Equipment"].unique().tolist()
x_coords = [2, 5, 8, 3, 6, 9]
y_coords = [8, 7, 6, 3, 3, 2]
z_coords = [0, 0, 0, 0, 0, 0]
coord_map = dict(zip(equipment_list, zip(x_coords, y_coords, z_coords)))

# Unique timestamps
time_steps = sorted(df["Timestamp"].unique())

# Placeholder for 3D plot
plot_area = st.empty()
alert_audio = st.empty()

if play:
    for ts in time_steps:
        snapshot = df[df["Timestamp"] == ts]
        colors = [color_map[status] for status in snapshot["Status"]]

        fig = go.Figure(data=[
            go.Scatter3d(
                x=[coord_map[eq][0] for eq in snapshot["Equipment"]],
                y=[coord_map[eq][1] for eq in snapshot["Equipment"]],
                z=[coord_map[eq][2] for eq in snapshot["Equipment"]],
                mode='markers+text',
                marker=dict(size=18, color=colors, opacity=0.85),
                text=snapshot["Equipment"],
                textposition="top center"
            )
        ])

        fig.update_layout(
            title=f"🕒 Time: {ts}",
            scene=dict(
                xaxis_title="X Axis",
                yaxis_title="Y Axis",
                zaxis_title="Height",
                aspectratio=dict(x=1, y=1, z=0.3),
                camera=dict(eye=dict(x=1.6, y=1.6, z=0.6))
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        plot_area.plotly_chart(fig, use_container_width=True)

        # Alert sound if warning
        if "Warning" in snapshot["Status"].values:
            alert_audio.audio("https://www.soundjay.com/button/beep-07.wav", format="audio/wav")
        else:
            alert_audio.empty()

        time.sleep(speed)
