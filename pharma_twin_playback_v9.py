
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Pharma Twin Playback", layout="wide")
st.title("📽️ Pharma Safety Twin Playback – v9 with External Siren Fallback")

# Load 5-min simulation dataset
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

# External siren MP3 (hosted and autoplay-enabled)
def play_external_siren():
    audio_html = '''
    <audio autoplay loop>
      <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    '''
    audio_area.markdown(audio_html, unsafe_allow_html=True)

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
            play_external_siren()
        else:
            audio_area.empty()

        time.sleep(speed)
