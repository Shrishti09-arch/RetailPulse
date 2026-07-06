import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def load_features_data():
    """
    Loads and lightly optimizes retailpulse_features.csv.

    This is the SINGLE shared loader for this dataset. Every page must
    import and call this function (instead of defining its own local
    pd.read_csv / load_data function) so Streamlit's cache stores only
    ONE copy of this ~47MB file in memory for the whole app session,
    rather than one copy per page.
    """
    root_dir = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root_dir / "data" / "processed" / "retailpulse_features.csv")

    # Downcast numeric dtypes to reduce memory footprint
    float_cols = data.select_dtypes(include="float64").columns
    data[float_cols] = data[float_cols].astype("float32")

    int_cols = data.select_dtypes(include="int64").columns
    data[int_cols] = data[int_cols].astype("int32")

    return data


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