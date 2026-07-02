from pathlib import Path
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

# Load data
df = pd.read_csv(
    BASE_DIR / "data/processed/forecast_data.csv"
)

df["ds"] = pd.to_datetime(df["ds"])

print("Dataset Shape:", df.shape)

# Train-Test Split (80-20)
split_idx = int(len(df) * 0.8)

train = df.iloc[:split_idx]
test = df.iloc[split_idx:]

print("Train:", train.shape)
print("Test :", test.shape)

# Model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)

model.fit(train)

# Forecast
future = model.make_future_dataframe(
    periods=len(test),
    freq="W"
)

forecast = model.predict(future)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

forecast[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].to_csv(
    BASE_DIR / "data/processed/prophet_forecast.csv",
    index=False
)

print("Forecast file saved successfully")

# Evaluation
predictions = forecast["yhat"].tail(len(test)).values
actuals = test["y"].values

mae = mean_absolute_error(actuals, predictions)
rmse = np.sqrt(mean_squared_error(actuals, predictions))
mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100

print("\nModel Performance")
print("------------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE:", round(mape, 2), "%")

# Save forecast
forecast.to_csv(
    BASE_DIR / "data/processed/prophet_forecast.csv",
    index=False
)

# Plot
fig = model.plot(forecast)

plt.title("RetailPulse Sales Forecast")

plt.savefig(
    BASE_DIR / "images/prophet_forecast.png"
)

plt.show()