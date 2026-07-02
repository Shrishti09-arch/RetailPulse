import streamlit as st

def sidebar_filters(df):

    st.sidebar.title("Retail Controls")

    store = st.sidebar.selectbox(
        "Store",
        ["All"] + sorted(df["Store"].unique())
    )

    dept = st.sidebar.selectbox(
        "Department",
        ["All"] + sorted(df["Dept"].unique())
    )

    if store != "All":
        df = df[df["Store"] == store]

    if dept != "All":
        df = df[df["Dept"] == dept]

    return df