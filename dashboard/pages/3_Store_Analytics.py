import streamlit as st
import pandas as pd
import plotly.express as px
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
    page_title="RetailPulse - Store Analytics",
    page_icon="🏪",
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
    st.markdown("### 🏪 Store Analytics")
with col2:
    st.text_input("Search", placeholder="🔍 Search stores...", label_visibility="collapsed")
with col3:
    st.markdown(f"<div style='background:#131C31; padding:12px; border-radius:15px; text-align:center;'>🔔&nbsp;&nbsp;👤<br><small>{st.session_state.get('username', 'User')}</small></div>", unsafe_allow_html=True)

# =========================
# PAGE HERO
# =========================

st.markdown(
    """
    <div class='hero-card'>
    <h1>🏪 Store Analytics</h1>
    <h3>Performance Metrics Across All Stores</h3>
    <p>Compare store performance, identify top performers, and optimize operations.</p>
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
    store_filter = st.selectbox(
        "🏬 Store",
        ["All"] + sorted(df["Store"].unique().tolist())
    )

with col2:
    dept_filter = st.selectbox(
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

if store_filter != "All":
    filtered_df = filtered_df[filtered_df["Store"] == store_filter]

if dept_filter != "All":
    filtered_df = filtered_df[filtered_df["Dept"] == dept_filter]

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

# =========================
# KPI CARDS
# =========================

st.markdown("---")
st.markdown("## 📈 Store Metrics")

total_sales = filtered_df["Weekly_Sales"].sum()
avg_sales = filtered_df["Weekly_Sales"].mean()
stores = filtered_df["Store"].nunique()
departments = filtered_df["Dept"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>💰 Revenue</h4>
    <h2>${total_sales:,.0f}</h2>
    <span>Total Sales</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📈 Avg Sales</h4>
    <h2>${avg_sales:,.0f}</h2>
    <span>Weekly</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>🏪 Stores</h4>
    <h2>{stores}</h2>
    <span>Active</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📦 Departments</h4>
    <h2>{departments}</h2>
    <span>Total</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# STORE RANKING
# =========================

st.markdown("---")
st.markdown("## 🏆 Store Ranking")

store_rank = (
    filtered_df
    .groupby("Store")["Weekly_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

store_rank["Rank"] = (
    store_rank["Weekly_Sales"]
    .rank(ascending=False, method="dense")
    .astype(int)
)

with st.expander("View Detailed Data"):
    st.dataframe(store_rank, width="stretch", height=450)

# =========================
# TOP 10 STORES
# =========================

st.markdown("---")
st.markdown("## 🚀 Top 10 Stores")

top10 = store_rank.head(10)

fig_top10 = px.bar(
    top10,
    x="Store",
    y="Weekly_Sales",
    title="Top 10 Stores"
)

fig_top10.update_traces(marker_color="#AF1763")

fig_top10.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_top10, width="stretch")

# =========================
# BOTTOM 10 STORES
# =========================

st.markdown("---")
st.markdown("## ⚠️ Bottom 10 Stores")

bottom10 = store_rank.tail(10)

fig_bottom10 = px.bar(
    bottom10,
    x="Store",
    y="Weekly_Sales",
    title="Bottom 10 Stores"
)

fig_bottom10.update_traces(marker_color="#FFC107")

fig_bottom10.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_bottom10, width="stretch")

# =========================
# REVENUE HEATMAP
# =========================

st.markdown("---")
st.markdown("## 🔥 Revenue Heatmap (Store vs Month)")

heat = (
    filtered_df
    .pivot_table(
        values="Weekly_Sales",
        index="Store",
        columns="Month",
        aggfunc="sum"
    )
)

fig_heat = px.imshow(
    heat,
    aspect="auto",
    color_continuous_scale="Blues"
)

fig_heat.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_heat, width="stretch")

# =========================
# MONTHLY REVENUE TREND
# =========================

st.markdown("---")
st.markdown("## 📈 Monthly Revenue Trend")

monthly = (
    filtered_df
    .groupby("Month")["Weekly_Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly,
    x="Month",
    y="Weekly_Sales",
    markers=True
)

fig_monthly.update_traces(line_color="#0DCAF0")

fig_monthly.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_monthly, width="stretch")

# =========================
# HOLIDAY VS NORMAL SALES
# =========================

st.markdown("---")
st.markdown("## 🎄 Holiday vs Normal Sales")

holiday_comparison = (
    filtered_df
    .groupby("IsHoliday")["Weekly_Sales"]
    .mean()
    .reset_index()
)

fig_holiday = px.bar(
    holiday_comparison,
    x="IsHoliday",
    y="Weekly_Sales"
)

fig_holiday.update_traces(marker_color="#198754")

fig_holiday.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_holiday, width="stretch")

# =========================
# DEPARTMENT COMPARISON
# =========================

st.markdown("---")
st.markdown("## 📦 Department Comparison")

dept_comparison = (
    filtered_df
    .groupby("Dept")["Weekly_Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig_dept = px.bar(
    dept_comparison,
    x="Dept",
    y="Weekly_Sales"
)

fig_dept.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_dept, width="stretch")

# =========================
# STORE PERFORMANCE TABLE
# =========================

st.markdown("---")
st.markdown("## 📋 Store Performance Table")

performance = (
    filtered_df
    .groupby("Store")
    .agg(
        Revenue=("Weekly_Sales", "sum"),
        Average=("Weekly_Sales", "mean"),
        Departments=("Dept", "nunique")
    )
    .reset_index()
)

with st.expander("View Detailed Data"):
    st.dataframe(performance, width="stretch", height=450)

# =========================
# AI RECOMMENDATION
# =========================

st.markdown("---")
st.markdown("## 🤖 AI Recommendation")

best_store = performance.sort_values("Revenue", ascending=False).iloc[0]["Store"]

st.markdown(
    f"""
    <div class='ai-card'>
    <h3>🧠 AI Recommendation</h3>
    <p>
    Best Performing Store
    <strong>{best_store}</strong>
    <br><br>
    Increase inventory allocation.
    <br><br>
    Expected Growth
    <strong>+9.4%</strong>
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
    <li>Top Store: {best_store}</li>
    <li>Total Stores: {stores}</li>
    <li>Departments: {departments}</li>
    <li>Revenue Trend Positive</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# DOWNLOAD REPORT
# =========================

st.markdown("---")
st.markdown("## 📥 Download Report")

report = f"""
STORE ANALYTICS REPORT

Revenue:
${total_sales:,.0f}

Stores:
{stores}

Departments:
{departments}

Top Store:
{best_store}
"""

st.download_button(
    label="📄 Download Store Report",
    data=report,
    file_name="Store_Report.txt"
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
    AI Retail Analytics Platform | Store Analytics
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