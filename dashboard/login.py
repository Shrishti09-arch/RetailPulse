import streamlit as st
from auth import *
from pathlib import Path

# Initialize database
create_users_table()

# Set page config
st.set_page_config(
    page_title="RetailPulse - Login",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load CSS
css_file = Path(__file__).resolve().parent / "assets" / "login.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Redirect if already logged in
if st.session_state.logged_in:
    st.switch_page("pages/0_Dashboard.py")

# ===========================
# MAIN LOGIN PAGE
# ===========================

# Create two columns
col1, col2 = st.columns([1, 1], gap="large")

# ===== LEFT SIDE: BRANDING =====
with col1:
    st.markdown("""
    <div class="login-brand">
        <div class="brand-icon">📈</div>
        <h1>RetailPulse</h1>
        <p class="brand-subtitle">AI-Powered Retail Analytics</p>
        <p class="brand-desc">Predict demand, monitor stores, optimize inventory with AI-driven insights.</p>
        
        <div class="features">
            <div class="feature-item">
                <span class="feature-icon">🔮</span>
                <div>
                    <strong>Demand Forecasting</strong>
                    <p>Accurate predictions</p>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <div>
                    <strong>Sales Analytics</strong>
                    <p>Real-time insights</p>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🤖</span>
                <div>
                    <strong>AI Recommendations</strong>
                    <p>Smart decisions</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== RIGHT SIDE: LOGIN FORM =====
with col2:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Tab selection
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # ===== LOGIN TAB =====
    with tab1:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        st.markdown('<h2 class="form-title">Welcome Back</h2>', unsafe_allow_html=True)
        st.markdown('<p class="form-subtitle">Enter your credentials to access the dashboard</p>', unsafe_allow_html=True)
        
        # Username input
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        
        # Password input
        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password",
            key="login_password"
        )
        
        # Remember me
        col_check, col_forgot = st.columns([1, 1])
        with col_check:
            remember_me = st.checkbox("Remember me", key="remember")
        
        # Login button
        if st.button("🚀 Login", use_container_width=True, key="login_btn"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful! Redirecting...")
                st.balloons()
                st.switch_page("pages/0_Dashboard.py")
            else:
                st.error("❌ Invalid username or password")
        
        # Divider
        st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
        
        # Create account link
        st.markdown(
            '<p class="form-footer">Don\'t have an account? <span class="switch-tab">Click "Sign Up" tab</span></p>',
            unsafe_allow_html=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== SIGNUP TAB =====
    with tab2:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        st.markdown('<h2 class="form-title">Create Account</h2>', unsafe_allow_html=True)
        st.markdown('<p class="form-subtitle">Join RetailPulse to get started</p>', unsafe_allow_html=True)
        
        # Username input
        new_username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="signup_username"
        )
        
        # Password input
        new_password = st.text_input(
            "Password",
            placeholder="Create a strong password",
            type="password",
            key="signup_password"
        )
        
        # Confirm password
        confirm_password = st.text_input(
            "Confirm Password",
            placeholder="Confirm your password",
            type="password",
            key="confirm_password"
        )
        
        # Terms checkbox
        agree_terms = st.checkbox("I agree to the Terms & Conditions", key="terms")
        
        # Sign up button
        if st.button("✨ Create Account", use_container_width=True, key="signup_btn"):
            if not new_username or not new_password:
                st.error("❌ Please fill all fields")
            elif new_password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not agree_terms:
                st.error("❌ Please agree to Terms & Conditions")
            else:
                if register_user(new_username, new_password):
                    st.success("✅ Account created successfully! You can now login.")
                else:
                    st.error("❌ Username already exists")
        
        # Divider
        st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
        
        # Login link
        st.markdown(
            '<p class="form-footer">Already have an account? <span class="switch-tab">Click "Login" tab</span></p>',
            unsafe_allow_html=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="login-footer">
        <p>© 2026 RetailPulse. All rights reserved.</p>
        <p style="font-size: 12px; opacity: 0.7;">Built with Streamlit & AI</p>
    </div>
""", unsafe_allow_html=True)