import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from auth import *

# =========================
# INITIALIZATION
# =========================

css_file = Path(__file__).resolve().parents[1] / "assets" / "style.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()

st.set_page_config(
    page_title="RetailPulse - Demand Forecasting",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("<div class='sidebar-title'>📈 RetailPulse</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='color:#A9B7D0; font-size:12px; text-transform:uppercase;'>Dashboard</h4>", unsafe_allow_html=True)
    st.page_link("pages/0_Dashboard.py", label="🏠 Dashboard")
    
    st.markdown("<h4 style='color:#A9B7D0; font-size:12px; text-transform:uppercase; margin-top:20px;'>Analytics</h4>", unsafe_allow_html=True)
    st.page_link("pages/1_Sales_Intelligence.py", label="📊 Sales Intelligence")
    st.page_link("pages/2_Demand_Forecasting.py", label="🔮 Demand Forecasting")
    st.page_link("pages/3_Store_Analytics.py", label="🏪 Store Analytics")
    
    st.markdown("<h4 style='color:#A9B7D0; font-size:12px; text-transform:uppercase; margin-top:20px;'>AI & Models</h4>", unsafe_allow_html=True)
    st.page_link("pages/4_AI_Insights.py", label="🤖 AI Insights")
    st.page_link("pages/5_Model_Performance.py", label="📈 Model Performance")
    
    st.markdown("<h4 style='color:#A9B7D0; font-size:12px; text-transform:uppercase; margin-top:20px;'>Operations</h4>", unsafe_allow_html=True)
    st.page_link("pages/6_Inventory_Optimizer.py", label="📦 Inventory Optimizer")
    st.page_link(
        "pages/7_Settings.py",
        label="⚙ Settings"
    )
    
    st.markdown("---")
    st.markdown(f"<div style='background: linear-gradient(135deg, #0D6EFD, #AF1763); padding:15px; border-radius:12px; text-align:center;'><p style='margin:0; color:white; font-weight:700;'>{st.session_state.get('username', 'User')}</p><p style='margin:5px 0 0 0; color:rgba(255,255,255,0.8); font-size:12px;'>Admin</p></div>", unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("dashboard/login.py")

# =========================
# NAVBAR
# =========================

col1, col2, col3 = st.columns([6, 4, 2])
with col1:
    st.markdown("### 🔮 Demand Forecasting")
with col2:
    st.text_input("Search", placeholder="🔍 Search forecasts...", label_visibility="collapsed")
with col3:
    st.markdown(f"<div style='background:#131C31; padding:12px; border-radius:15px; text-align:center;'>🔔&nbsp;&nbsp;👤<br><small>{st.session_state.get('username', 'User')}</small></div>", unsafe_allow_html=True)

# =========================
# PAGE HERO
# =========================

st.markdown(
    """
    <div class='hero-card'>
    <h1>🔮 Demand Forecasting</h1>
    <h3>AI-Powered Sales Predictions</h3>
    <p>Predict future demand with confidence intervals and machine learning models.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# DATA LOADING
# =========================

ROOT_DIR = Path(__file__).resolve().parents[2]

with st.spinner("Loading Forecast Data..."):
    try:
        forecast = pd.read_csv(ROOT_DIR / "data" / "processed" / "prophet_forecast.csv")
    except FileNotFoundError:
        st.error("Dataset not found.")
        st.stop()

forecast["ds"] = pd.to_datetime(forecast["ds"])

# =========================
# FILTERS
# =========================

st.markdown("---")
st.markdown("## 🔍 Filters")

date_range = st.date_input(
    "📅 Date Range",
    value=(forecast["ds"].min(), forecast["ds"].max())
)

filtered_forecast = forecast.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_forecast = filtered_forecast[
        (filtered_forecast["ds"] >= pd.to_datetime(start_date))
        & (filtered_forecast["ds"] <= pd.to_datetime(end_date))
    ]

st.info(f"Showing {len(filtered_forecast):,} records after applying filters.")
st.toast("Filters Applied Successfully ✅")

if st.button("🔄 Reset Filters"):
    st.rerun()

if filtered_forecast.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# =========================
# FORECAST SETTINGS
# =========================

st.markdown("## ⚙ Forecast Settings")

col1, col2 = st.columns(2)

with col1:
    horizon = st.selectbox(
        "Forecast Horizon",
        ["30 Days", "60 Days", "90 Days"]
    )

with col2:
    show_ci = st.toggle(
        "Show Confidence Interval",
        value=True
    )

if horizon == "30 Days":
    forecast_display = filtered_forecast.head(30)
elif horizon == "60 Days":
    forecast_display = filtered_forecast.head(60)
else:
    forecast_display = filtered_forecast.head(90)

# =========================
# FORECAST KPI CARDS
# =========================

st.markdown("---")
st.markdown("## 📊 Forecast Metrics")

forecast_sales = forecast_display["yhat"].sum()
avg_forecast = forecast_display["yhat"].mean()
highest_forecast = forecast_display["yhat"].max()
lowest_forecast = forecast_display["yhat"].min()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📈 Forecast Revenue</h4>
    <h2>${forecast_sales:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📊 Average Forecast</h4>
    <h2>${avg_forecast:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>🚀 Highest Forecast</h4>
    <h2>${highest_forecast:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📉 Lowest Forecast</h4>
    <h2>${lowest_forecast:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FORECAST CHART
# =========================

st.markdown("---")
st.markdown("## 📈 Sales Forecast")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=forecast_display["ds"],
        y=forecast_display["yhat"],
        mode="lines",
        name="Forecast",
        line=dict(color="#0DCAF0", width=4)
    )
)

if show_ci:
    fig.add_trace(
        go.Scatter(
            x=forecast_display["ds"],
            y=forecast_display["yhat_upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_display["ds"],
            y=forecast_display["yhat_lower"],
            mode="lines",
            fill="tonexty",
            line=dict(width=0),
            name="Confidence Interval",
            fillcolor="rgba(13, 206, 240, 0.2)"
        )
    )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    hovermode="x unified",
    height=550,
    title="Future Sales Forecast",
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# FORECAST SUMMARY
# =========================

st.markdown("## 📋 Forecast Summary")

growth = (
    (
        forecast_display.iloc[-1]["yhat"]
        - forecast_display.iloc[0]["yhat"]
    )
    / forecast_display.iloc[0]["yhat"]
) * 100

st.markdown(
    f"""
    <div class='executive-card'>
    <h3>Forecast Summary</h3>
    <ul>
    <li>Total Forecast Revenue: ${forecast_sales:,.0f}</li>
    <li>Average Forecast: ${avg_forecast:,.0f}</li>
    <li>Expected Growth: {growth:.2f}%</li>
    <li>Forecast Horizon: {horizon}</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# FORECAST STATISTICS
# =========================

st.markdown("---")
st.markdown("## 📐 Forecast Statistics")

stats = pd.DataFrame({
    "Metric": [
        "Minimum",
        "Maximum",
        "Average",
        "Median",
        "Std Dev"
    ],
    "Value": [
        forecast_display["yhat"].min(),
        forecast_display["yhat"].max(),
        forecast_display["yhat"].mean(),
        forecast_display["yhat"].median(),
        forecast_display["yhat"].std()
    ]
})

with st.expander("View Detailed Data"):
    st.dataframe(stats, use_container_width=True, height=450)

# =========================
# DOWNLOAD FORECAST CSV
# =========================

st.markdown("---")
st.markdown("## 📥 Download Forecast")

csv = forecast_display.to_csv(index=False).encode()

st.download_button(
    label="⬇ Download Forecast CSV",
    data=csv,
    file_name="Forecast.csv",
    mime="text/csv"
)

# =========================
# DOWNLOAD FORECAST REPORT
# =========================

report = f"""
FORECAST REPORT

Forecast Horizon
{horizon}

Forecast Revenue
${forecast_sales:,.0f}

Average Forecast
${avg_forecast:,.0f}

Growth
{growth:.2f}%

Highest Forecast
${highest_forecast:,.0f}

Lowest Forecast
${lowest_forecast:,.0f}
"""

st.download_button(
    label="📄 Download Forecast Report",
    data=report,
    file_name="Forecast_Report.txt"
)

# =========================
# AI RECOMMENDATION
# =========================

st.markdown("---")
st.markdown("## 🧠 AI Recommendations")

st.markdown(
    f"""
    <div class='ai-card'>
    <h3>🧠 AI Recommendation</h3>
    <p>
    Demand is expected to
    <strong>increase by {growth:.2f}%</strong>
    <br><br>
    Increase inventory before the next {horizon} to avoid stock shortages.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# EXECUTIVE SUMMARY
# =========================

st.markdown(
    f"""
    <div class='executive-card'>
    <h3>Executive Summary</h3>
    <ul>
    <li>Total Forecast Revenue: ${forecast_sales:,.0f}</li>
    <li>Growth Rate: {growth:.2f}%</li>
    <li>Forecast Horizon: {horizon}</li>
    <li>Confidence Interval Available</li>
    <li>Recommendation: Increase inventory</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# FOOTER
# =========================

st.markdown("---")
st.markdown(
    """
    <center>
    <hr>
    <h3 style="color:#FFFFFF;">RetailPulse</h3>
    <p style="color:#A9B7D0; font-size:12px;">
    AI Retail Analytics Platform | Demand Forecasting
    </p>
    <p style="color:#A9B7D0; font-size:12px;">
    Version 2.0
    </p>
    <p style="color:#A9B7D0; font-size:12px;">
    Built using Python · Streamlit · Prophet · XGBoost · SQLite
    </p>
    <p style="color:#A9B7D0; font-size:12px;">
    ©2026 RetailPulse
    </p>
    </center>
    """,
    unsafe_allow_html=True
)