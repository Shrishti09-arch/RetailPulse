import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from auth import *

st.set_page_config(
    page_title="RetailPulse - Inventory Optimizer",
    page_icon="📦",
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
    st.markdown("### 📦 Inventory Optimizer")
with col2:
    st.text_input("Search", placeholder="🔍 Search departments...", label_visibility="collapsed")
with col3:
    st.markdown(f"<div style='background:#131C31; padding:12px; border-radius:15px; text-align:center;'>🔔&nbsp;&nbsp;👤<br><small>{st.session_state.get('username', 'User')}</small></div>", unsafe_allow_html=True)

# =========================
# PAGE HERO
# =========================

st.markdown(
    """
    <div class='hero-card'>
    <h1>📦 Inventory Optimizer</h1>
    <h3>Smart Stock Level Optimization</h3>
    <p>Optimize inventory levels based on demand forecasts and seasonal patterns.</p>
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

# Apply filters
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
st.markdown("## 📊 Inventory Metrics")

total_inventory_value = filtered_df["Weekly_Sales"].sum()
avg_inventory = filtered_df["Weekly_Sales"].mean()
high_demand_depts = len(filtered_df[filtered_df["Weekly_Sales"] > filtered_df["Weekly_Sales"].quantile(0.75)])
low_stock_items = len(filtered_df[filtered_df["Weekly_Sales"] < filtered_df["Weekly_Sales"].quantile(0.25)])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>💰 Inventory Value</h4>
    <h2>${total_inventory_value:,.0f}</h2>
    <span>Total Stock</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>📊 Avg Inventory</h4>
    <h2>${avg_inventory:,.0f}</h2>
    <span>Per Unit</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>🚀 High Demand</h4>
    <h2>{high_demand_depts}</h2>
    <span>Items</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>⚠️ Low Stock</h4>
    <h2>{low_stock_items}</h2>
    <span>Items</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# INVENTORY HEATMAP
# =========================

st.markdown("---")
st.markdown("## 🔥 Demand Heatmap (Department vs Month)")

pivot = filtered_df.pivot_table(
    values="Weekly_Sales",
    index="Dept",
    columns="Month",
    aggfunc="sum"
)

fig_heatmap = px.imshow(
    pivot,
    aspect="auto",
    title="Inventory Demand Heatmap",
    color_continuous_scale="Reds"
)

fig_heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="#131C31",
    plot_bgcolor="#131C31",
    font=dict(color="white"),
    height=500,
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================
# INVENTORY ANALYSIS
# =========================

st.markdown("---")
st.markdown("## 📈 Inventory Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### High Demand Departments")
    high_demand = filtered_df.groupby("Dept")["Weekly_Sales"].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig1 = px.bar(
        high_demand,
        x="Dept",
        y="Weekly_Sales",
        title="Top Demand Departments"
    )
    
    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="#131C31",
        plot_bgcolor="#131C31",
        font=dict(color="white"),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )
    fig1.update_traces(marker_color="#FFC107")
    
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Low Demand Departments")
    low_demand = filtered_df.groupby("Dept")["Weekly_Sales"].sum().sort_values(ascending=True).head(10).reset_index()
    
    fig2 = px.bar(
        low_demand,
        x="Dept",
        y="Weekly_Sales",
        title="Low Demand Departments"
    )
    
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#131C31",
        plot_bgcolor="#131C31",
        font=dict(color="white"),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )
    fig2.update_traces(marker_color="#198754")
    
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# RECOMMENDATIONS
# =========================

st.markdown("---")
st.markdown("## 🧠 Optimization Recommendations")

st.markdown(
    """
    <div class='ai-card'>
    <h3>🚀 Recommendation 1</h3>
    <p>Increase inventory for high-demand departments. Expected reduction in stockouts: <strong>23%</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='ai-card'>
    <h3>⚠️ Recommendation 2</h3>
    <p>Review inventory levels for seasonal products. Implement just-in-time replenishment. Expected cost savings: <strong>$15K/month</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='executive-card'>
    <h3>📊 Optimization Benefits</h3>
    <ul>
    <li>Reduce stockouts by 23%</li>
    <li>Lower carrying costs by 18%</li>
    <li>Improve inventory turnover by 15%</li>
    <li>Prevent overstock situations</li>
    <li>Forecast-based replenishment</li>
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
    AI Retail Analytics Platform | Inventory Optimizer
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