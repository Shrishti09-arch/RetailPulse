from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

print("Loading datasets...")

train = pd.read_csv(
    BASE_DIR / "data/raw/train.csv",
    parse_dates=["Date"]
)

features = pd.read_csv(
    BASE_DIR / "data/raw/features.csv",
    parse_dates=["Date"]
)

stores = pd.read_csv(
    BASE_DIR / "data/raw/stores.csv"
)

print("Merging datasets...")

df = train.merge(
    features,
    on=["Store", "Date", "IsHoliday"],
    how="left"
)

df = df.merge(
    stores,
    on="Store",
    how="left"
)

print("\nMerged Shape:", df.shape)

# Missing values
markdown_cols = [
    "MarkDown1",
    "MarkDown2",
    "MarkDown3",
    "MarkDown4",
    "MarkDown5"
]

for col in markdown_cols:
    df[col] = df[col].fillna(0)

df["CPI"] = df["CPI"].fillna(df["CPI"].median())
df["Unemployment"] = df["Unemployment"].fillna(
    df["Unemployment"].median()
)

# Remove duplicates
df = df.drop_duplicates()

print("\nFinal Shape:", df.shape)

output_path = (
    BASE_DIR /
    "data/processed/retailpulse_master.csv"
)

df.to_csv(output_path, index=False)

print("\nSaved Successfully")
print(output_path)