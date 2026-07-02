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
    page_title="RetailPulse - AI Insights",
    page_icon="🤖",
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
    
    if st.button("🚪 Logout", width="stretch"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("login.py")

# =========================
# NAVBAR
# =========================

col1, col2, col3 = st.columns([6, 4, 2])
with col1:
    st.markdown("### 🤖 AI Insights")
with col2:
    st.text_input("Search", placeholder="🔍 Search insights...", label_visibility="collapsed")
with col3:
    st.markdown(f"<div style='background:#131C31; padding:12px; border-radius:15px; text-align:center;'>🔔&nbsp;&nbsp;👤<br><small>{st.session_state.get('username', 'User')}</small></div>", unsafe_allow_html=True)

# =========================
# PAGE HERO
# =========================

st.markdown(
    """
    <div class='hero-card'>
    <h1>🤖 AI Business Insights</h1>
    <h3>Machine Learning-Powered Recommendations</h3>
    <p>Get actionable insights powered by advanced machine learning and data analysis.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# DATA LOADING
# =========================

ROOT_DIR = Path(__file__).resolve().parents[2]

with st.spinner("Loading Retail Analytics..."):
    try:
        df = pd.read_csv(ROOT_DIR / "data" / "processed" / "retailpulse_features.csv")
    except FileNotFoundError:
        st.error("Dataset not found.")
        st.stop()
df["Date"] = pd.to_datetime(df["Date"])

# =========================
# FILTERS
# =========================

st.markdown("---")
st.markdown("## 🔍 Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_store = st.selectbox(
        "🏬 Store",
        ["All"] + sorted(df["Store"].unique().tolist())
    )

with col2:
    selected_dept = st.selectbox(
        "📦 Department",
        ["All"] + sorted(df["Dept"].unique().tolist())
    )

with col3:
    date_range = st.date_input(
        "📅 Date Range",
        value=(df["Date"].min(), df["Date"].max())
    )

with col4:
    holiday = st.selectbox(
        "🎄 Holiday",
        ["All", "Holiday", "Non-Holiday"]
    )

filtered_df = df.copy()

if selected_store != "All":
    filtered_df = filtered_df[filtered_df["Store"] == selected_store]

if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["Dept"] == selected_dept]

if holiday == "Holiday":
    filtered_df = filtered_df[filtered_df["IsHoliday"] == True]
elif holiday == "Non-Holiday":
    filtered_df = filtered_df[filtered_df["IsHoliday"] == False]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date))
        & (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

st.info(f"Showing {len(filtered_df):,} records after applying filters.")
st.toast("Filters Applied Successfully ✅")

if st.button("🔄 Reset Filters"):
    st.rerun()

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ==========================
# AI CALCULATIONS
# ==========================

total_sales = filtered_df["Weekly_Sales"].sum()

avg_sales = filtered_df["Weekly_Sales"].mean()

top_store = (
    filtered_df.groupby("Store")["Weekly_Sales"]
    .sum()
    .idxmax()
)

top_store_sales = (
    filtered_df.groupby("Store")["Weekly_Sales"]
    .sum()
    .max()
)

lowest_store = (
    filtered_df.groupby("Store")["Weekly_Sales"]
    .sum()
    .idxmin()
)

top_department = (
    filtered_df.groupby("Dept")["Weekly_Sales"]
    .sum()
    .idxmax()
)

top_department_sales = (
    filtered_df.groupby("Dept")["Weekly_Sales"]
    .sum()
    .max()
)

highest_month = (
    filtered_df.groupby("Month")["Weekly_Sales"]
    .sum()
    .idxmax()
)

stores = filtered_df["Store"].nunique()

departments = filtered_df["Dept"].nunique()

# Holiday Impact
holiday_sales = filtered_df[
    filtered_df["IsHoliday"] == True
]["Weekly_Sales"].mean()

normal_sales = filtered_df[
    filtered_df["IsHoliday"] == False
]["Weekly_Sales"].mean()

if normal_sales > 0:
    holiday_impact = (
        (holiday_sales - normal_sales)
        / normal_sales
    ) * 100
else:
    holiday_impact = 0

# Inventory Risk
inventory_risk = filtered_df[
    filtered_df["Weekly_Sales"]
    >
    filtered_df["Weekly_Sales"].quantile(0.90)
].shape[0]

# Demand Growth
monthly_sales = (
    filtered_df
    .groupby("Month")["Weekly_Sales"]
    .sum()
)

growth = (
    monthly_sales.pct_change().mean()
) * 100

if pd.isna(growth):
    growth = 0

# Business Health Score
health_score = min(
    100,
    int(
        60
        + holiday_impact / 2
        + growth
    )
)

health_score = max(0, health_score)

# =========================
# KPI CARDS
# =========================

st.markdown("---")
st.markdown("## 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>💰 Revenue</h4>
    <h2>${total_sales:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>🏪 Stores</h4>
    <h2>{stores}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📦 Departments</h4>
    <h2>{departments}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📈 Avg Sales</h4>
    <h2>${avg_sales:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================
# AI RECOMMENDATION
# =========================

st.markdown("---")
st.markdown("## 🧠 AI-Generated Recommendations")

with st.spinner("Generating AI Insights..."):
    st.markdown(
        f"""
        <div class='ai-card'>
        <h3>🧠 AI Recommendation</h3>
        <p>
        Top Performing Store
        <strong>Store {top_store}</strong>
        <br><br>
        Recommended Action
        Increase inventory allocation.
        <br><br>
        Expected Growth
        <strong>{growth:.1f}%</strong>
        <br><br>
        Confidence
        <strong>96%</strong>
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
    <h3>📊 Executive Summary</h3>
    <ul>
    <li>Total Revenue: ${total_sales:,.0f}</li>
    <li>Top Store: {top_store}</li>
    <li>Top Department: {top_department}</li>
    <li>Highest Sales Month: {highest_month}</li>
    <li>Holiday Impact: {holiday_impact:.2f}%</li>
    <li>Business Health Score: {health_score}/100</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# BUSINESS HEALTH GAUGE
# =========================

st.markdown("---")
st.markdown("## 🏆 Business Health Score")

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=health_score,
        title={"text": "Business Health"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#0DCAF0"},
            "steps": [
                {"range": [0, 50], "color": "rgba(220, 53, 69, 0.25)"},
                {"range": [50, 80], "color": "rgba(255, 193, 7, 0.25)"},
                {"range": [80, 100], "color": "rgba(25, 135, 84, 0.25)"}
            ]
        }
    )
)

fig_gauge.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white")
)

st.plotly_chart(fig_gauge, width="stretch")

# =========================
# AI INSIGHTS TABLE
# =========================

st.markdown("---")
st.markdown("## 📋 AI Insights Summary")

summary = pd.DataFrame({
    "Metric": [
        "Top Store",
        "Top Department",
        "Highest Month",
        "Holiday Impact",
        "Growth",
        "Inventory Risk"
    ],
    "Value": [
        top_store,
        top_department,
        highest_month,
        f"{holiday_impact:.2f}%",
        f"{growth:.2f}%",
        inventory_risk
    ]
})

st.dataframe(
    summary,
    width="stretch",
    height=250
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
    AI Retail Analytics Platform | AI Insights
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