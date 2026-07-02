from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR /
    "data/processed/retailpulse_master.csv",
    parse_dates=["Date"]
)

print("Creating features...")

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Week"] = df["Date"].dt.isocalendar().week

df["Quarter"] = df["Date"].dt.quarter

df["DayOfWeek"] = df["Date"].dt.dayofweek

df["Weekend"] = (
    df["DayOfWeek"] >= 5
).astype(int)

df["Month_Start"] = (
    df["Date"].dt.is_month_start
).astype(int)

df["Month_End"] = (
    df["Date"].dt.is_month_end
).astype(int)

output_path = (
    BASE_DIR /
    "data/processed/retailpulse_features.csv"
)

df.to_csv(output_path, index=False)

print("Feature Engineering Complete")