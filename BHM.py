import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime 
from streamlit_autorefresh import st_autorefresh

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="BHOOMI Rockfall AI", page_icon="🤖", layout="wide")

st.markdown(""" 
    <style> 
    body { background-color: #0d1117; } 
    .block-container { padding-top: 1rem; padding-bottom: 1rem; } 
    </style> 
""", unsafe_allow_html=True)

# -------------------- AUTO REFRESH --------------------
st_autorefresh(interval=60000, key="refresh")

# -------------------- SIMULATED DATA --------------------
np.random.seed(datetime.now().second)
data = {
    "Timestamp": pd.date_range(datetime.now().replace(microsecond=0), periods=50, freq="s"),
    "Vibration": np.random.randint(10, 100, 50),
    "Temperature": np.random.randint(20, 80, 50),
}
df = pd.DataFrame(data)
current_risk = int(np.random.randint(0, 100))

# -------------------- LAYOUT --------------------
st.title("🤖 BHOOMI Rockfall AI Dashboard")

col_a, col_b, col_c = st.columns(3)

# -------------------- VIBRATION TREND --------------------
with col_a:
    st.subheader("📈 Vibration Trend")
    fig_vibration = px.line(df, x="Timestamp", y="Vibration", markers=True,
                            title="Vibration Levels", line_shape="spline",
                            color_discrete_sequence=["orange"])
    fig_vibration.update_layout(template="plotly_dark",
                                plot_bgcolor="#0d1117", paper_bgcolor="#0d1117")
    # Add High and Low threshold bands
    fig_vibration.add_hrect(
        y0=70, y1=100, fillcolor="red", opacity=0.2, line_width=0,
        annotation_text="High Risk", annotation_position="top left"
    )
    fig_vibration.add_hrect(
        y0=0, y1=30, fillcolor="green", opacity=0.2, line_width=0,
        annotation_text="Low Risk", annotation_position="bottom left"
    )
    st.plotly_chart(fig_vibration, use_container_width=True)

# -------------------- TEMPERATURE --------------------
with col_b:
    st.subheader("🌡 Temperature / Risk Level")
    fig_temp = px.bar(x=[""], y=[df["Temperature"].iloc[-1]], 
                      labels={"x": "", "y": "Temperature"},
                      color_discrete_sequence=["#FF7F0E"])
    fig_temp.update_layout(template="plotly_dark",
                           plot_bgcolor="#0d1117", paper_bgcolor="#0d1117")
    st.plotly_chart(fig_temp, use_container_width=True)

# -------------------- RISK METER --------------------
with col_c:
    st.subheader("⚠ Risk Probability Meter")
    fig_meter = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_risk,
        title={"text": "Current Risk"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "orange"},
            "steps": [
                {"range": [0, 40], "color": "green"},
                {"range": [40, 70], "color": "yellow"},
                {"range": [70, 100], "color": "red"}
            ],
        }
    ))
    fig_meter.update_layout(template="plotly_dark",
                            plot_bgcolor="#0d1117", paper_bgcolor="#0d1117")
    st.plotly_chart(fig_meter, use_container_width=True)

# -------------------- THERMAL HEATMAP LINKED TO RESTRICTED ZONE --------------------
st.subheader("🌡 Thermal Heatmap with Restricted Zone Overlay")
heat_data = np.random.normal(loc=current_risk, scale=15, size=(100, 100))
heat_data = np.clip(heat_data, 0, 100)

heat_fig = px.imshow(
    heat_data,
    color_continuous_scale="plasma",
    origin="lower",
    aspect="auto",
    labels=dict(color="Temperature / Risk Level"),
    title="Thermal Map with Restricted Zone",
    zmin=0, zmax=100
)

# Add restricted zone rectangle (hot area)
heat_fig.add_shape(
    type="rect",
    x0=30, x1=70,
    y0=40, y1=80,
    line=dict(color="red", width=2),
    fillcolor="rgba(255,0,0,0.3)"
)

# Add workers on heatmap
worker_x = np.random.randint(0, 100, 5)
worker_y = np.random.randint(0, 100, 5)
heat_fig.add_trace(go.Scatter(
    x=worker_x, y=worker_y,
    mode="markers+text",
    marker=dict(size=10, color="black", symbol="circle"),
    text=[f"Worker {i+1}" for i in range(5)],
    textposition="top center",
    name="Workers"
))

# Force axes to 0–100
heat_fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#0d1117",
    paper_bgcolor="#0d1117",
    xaxis=dict(range=[0,100]),
    yaxis=dict(range=[0,100]),
    margin=dict(r=80)
)

st.plotly_chart(heat_fig, use_container_width=True)
