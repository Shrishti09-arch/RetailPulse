import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from auth import *

st.set_page_config(
    page_title="RetailPulse - Model Performance",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# INITIALIZATION
# =========================

css_file = Path(__file__).resolve().parents[1] / "assets" / "style.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()

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
        st.switch_page("login.py")

# =========================
# NAVBAR
# =========================

col1, col2, col3 = st.columns([6, 4, 2])
with col1:
    st.markdown("### 📈 Model Performance")
with col2:
    st.text_input("Search", placeholder="🔍 Search models...", label_visibility="collapsed")
with col3:
    st.markdown(f"<div style='background:#131C31; padding:12px; border-radius:15px; text-align:center;'>🔔&nbsp;&nbsp;👤<br><small>{st.session_state.get('username', 'User')}</small></div>", unsafe_allow_html=True)

# =========================
# PAGE HERO
# =========================

st.markdown(
    """
    <div class='hero-card'>
    <h1>📈 Model Performance</h1>
    <h3>ML Model Evaluation & Comparison</h3>
    <p>Monitor and compare the performance of different forecasting models.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD PREDICTIONS
# =========================

ROOT_DIR = Path(__file__).resolve().parents[2]

with st.spinner("Loading Model Predictions..."):
    try:
        predictions = pd.read_csv(ROOT_DIR / "data" / "processed" / "predictions.csv")
    except FileNotFoundError:
        st.error("Dataset not found.")
        st.stop()

actual = predictions["Actual"]
pred = predictions["Predicted"]

# =========================
# CALCULATE METRICS
# =========================

mae = mean_absolute_error(actual, pred)

rmse = np.sqrt(mean_squared_error(actual, pred))

mape = np.mean(np.abs((actual - pred) / actual)) * 100

r2 = r2_score(actual, pred)

# =========================
# KPI CARDS
# =========================

st.markdown("---")
st.markdown("## 📊 Model Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📉 RMSE</h4>
    <h2>{rmse:.2f}</h2>
    <span>Lower is Better</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📊 MAE</h4>
    <h2>{mae:.2f}</h2>
    <span>Prediction Error</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>🎯 MAPE</h4>
    <h2>{mape:.2f}%</h2>
    <span>Accuracy Measure</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>🚀 R² Score</h4>
    <h2>{r2:.3f}</h2>
    <span>Model Fit</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ACTUAL VS PREDICTED
# =========================

st.markdown("---")
st.markdown("## 📈 Actual vs Predicted")

fig_actual_pred = px.line(
    predictions,
    y=["Actual", "Predicted"],
    title="Actual vs Predicted Sales"
)

fig_actual_pred.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_actual_pred, use_container_width=True)

# =========================
# RESIDUAL PLOT
# =========================

st.markdown("---")
st.markdown("## 📉 Residual Plot")

predictions["Residual"] = predictions["Actual"] - predictions["Predicted"]

fig_residual = px.scatter(
    predictions,
    x="Predicted",
    y="Residual",
    title="Residual Plot"
)

fig_residual.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_residual, use_container_width=True)

# =========================
# ERROR DISTRIBUTION
# =========================

st.markdown("---")
st.markdown("## 📊 Error Distribution")

fig_error_dist = px.histogram(
    predictions,
    x="Residual",
    nbins=30,
    title="Prediction Error Distribution"
)

fig_error_dist.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_error_dist, use_container_width=True)

# =========================
# MODEL COMPARISON TABLE
# =========================

st.markdown("---")
st.markdown("## 📋 Model Comparison Table")

comparison = pd.DataFrame({
    "Model": ["Prophet", "XGBoost"],
    "RMSE": [rmse, 1320],
    "MAE": [mae, 980],
    "MAPE": [mape, 8.2],
    "R²": [r2, 0.94]
})

with st.expander("View Detailed Data"):
    st.dataframe(comparison, use_container_width=True, height=250)

# =========================
# AI MODEL INSIGHTS
# =========================

st.markdown("---")
st.markdown("## 🧠 Model Recommendation")

st.markdown(
    f"""
    <div class='ai-card'>
    <h3>🧠 Model Insights</h3>
    <p>
    Current Best Model
    <strong>Prophet</strong>
    <br><br>
    Forecast Accuracy
    <strong>{100 - mape:.2f}%</strong>
    <br><br>
    Recommendation
    Continue weekly retraining.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='executive-card'>
    <h3>📊 Model Performance Summary</h3>
    <ul>
    <li><strong>Prophet</strong> - Good for seasonal data analysis</li>
    <li><strong>XGBoost</strong> - Placeholder comparison values, replace with real results once trained</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# DOWNLOAD METRICS
# =========================

st.markdown("---")
st.markdown("## 📥 Download Metrics")

report = f"""
MODEL PERFORMANCE REPORT

RMSE : {rmse:.2f}

MAE : {mae:.2f}

MAPE : {mape:.2f}

R2 : {r2:.3f}
"""

st.download_button(
    label="📄 Download Metrics",
    data=report,
    file_name="Model_Report.txt",
    mime="text/plain"
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
    AI Retail Analytics Platform | Model Performance
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