from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "data/processed/retailpulse_features.csv",
    parse_dates=["Date"]
)

forecast_df = (
    df.groupby("Date")["Weekly_Sales"]
      .sum()
      .reset_index()
)

forecast_df.columns = ["ds", "y"]

output_file = BASE_DIR / "data/processed/forecast_data.csv"

forecast_df.to_csv(output_file, index=False)

print("Forecast dataset created successfully!")
print("Shape:", forecast_df.shape)
print("\nFirst 5 rows:")
print(forecast_df.head())
print("\nSaved to:", output_file)