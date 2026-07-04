import streamlit as st
from pathlib import Path
from auth import *

if not st.session_state.get("logged_in", False):
    st.switch_page("dashboard/login.py")

css_file = Path(__file__).resolve().parents[1] / "assets" / "style.css"

with open(css_file) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="RetailPulse Settings",
    page_icon="⚙",
    layout="wide"
)

#sidebar
with st.sidebar:

    st.markdown(
        "<div class='sidebar-title'>📈 RetailPulse</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.page_link(
        "pages/0_Dashboard.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/1_Sales_Intelligence.py",
        label="📊 Sales Intelligence"
    )

    st.page_link(
        "pages/2_Demand_Forecasting.py",
        label="🔮 Demand Forecasting"
    )

    st.page_link(
        "pages/3_Store_Analytics.py",
        label="🏪 Store Analytics"
    )

    st.page_link(
        "pages/4_AI_Insights.py",
        label="🤖 AI Insights"
    )

    st.page_link(
        "pages/5_Model_Performance.py",
        label="📈 Model Performance"
    )

    st.page_link(
        "pages/6_Inventory_Optimizer.py",
        label="📦 Inventory Optimizer"
    )

    st.page_link(
        "pages/7_Settings.py",
        label="⚙ Settings"
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div class='nav-profile'>
        👤
        <br>
        {st.session_state.username}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("dashboard/login.py")

#navbar
nav1, nav2, nav3 = st.columns([5, 5, 2])

with nav1:
    st.markdown("## 📈 RetailPulse")

with nav2:
    st.text_input(
        "Search",
        placeholder="🔍 Search stores...",
        label_visibility="collapsed"
    )

with nav3:
    st.markdown(
        f"""
        <div class='nav-profile'>
        🔔
        <br>
        👤
        <br>
        {st.session_state.username}
        </div>
        """,
        unsafe_allow_html=True
    )

#hero banner 
st.markdown("""
<div class="hero-card">

<h1>⚙ Settings</h1>

<h3>
Customize your RetailPulse experience
</h3>

<p>

Manage profile,
notifications,
themes,
security,
and export preferences.

</p>

</div>
""",
unsafe_allow_html=True)

#profile card
st.markdown("## 👤 Profile")

col1,col2=st.columns([2,3])

#left
st.image(
    "https://ui-avatars.com/api/?name=Admin",
    width=150
)

#right
st.markdown(f"""
<div class='executive-card'>

<h3>{st.session_state.username}</h3>

<p>

Role : Administrator

Department : Retail Analytics

Status : Active

</p>

</div>
""",
unsafe_allow_html=True)

#theme settings
theme = st.selectbox(

"Theme",

[
"Dark",
"Light",
"System"
]

)

#notifications
email_notifications = st.toggle(
    "Email Notifications",
    True
)

forecast_alerts = st.toggle(
    "Forecast Alerts",
    True
)

inventory_alerts = st.toggle(
    "Inventory Alerts",
    True
)

#language
language = st.selectbox(

"Language",

[
"English",
"Hindi",
"French",
"German"
]

)

#export preference
format_choice = st.radio(

"Default Export Format",

[
"CSV",
"Excel",
"PDF"
]

)

#security
st.checkbox(
    "Require Login Authentication",
    True
)

st.checkbox(
    "Enable Session Timeout",
    False
)

st.checkbox(
    "Remember Login",
    True
)

#about section (descriptive)
st.markdown("---")
st.markdown("""
## About RetailPulse

RetailPulse is an AI-powered Retail Analytics Platform that combines demand forecasting, sales intelligence, inventory optimization, AI insights, and model performance monitoring into a single dashboard.
""")

#about card
st.markdown("""
<div class='executive-card'>

<h3>About RetailPulse</h3>

<ul>

<li>Version : 2.0</li>

<li>Developer : Shrishti Vaishnav</li>

<li>Framework : Streamlit</li>

<li>Machine Learning : XGBoost + Prophet</li>

<li>Database : SQLite</li>

</ul>

</div>
""",
unsafe_allow_html=True)

#sys info
st.markdown("## 💻 System Information")
st.info(f"""

Python

3.14

Streamlit

1.58

User

{st.session_state.username}

""")

#save / reset buttons
save_col, reset_col = st.columns(2)

with save_col:
    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):
        st.toast("Settings Saved Successfully ✅")
        st.success(
            "Settings saved successfully!"
        )

with reset_col:
    if st.button(
        "🔄 Reset Settings",
        use_container_width=True
    ):
        st.toast("Settings Reset ✅")
        st.info(
            "Settings have been reset to default."
        )

#footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<hr>
<div style='text-align:center;'>
<h3>RetailPulse</h3>
<p>AI Retail Analytics Platform | Settings</p>
<p>Version 2.0</p>
<p>Built using Python · Streamlit · Prophet · XGBoost · SQLite</p>
<p>©2026 RetailPulse</p>
</div>
""", unsafe_allow_html=True)