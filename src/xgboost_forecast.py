from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR /
    "data/processed/retailpulse_features.csv"
)

# Features
X = df[
    [
        "Store",
        "Dept",
        "Temperature",
        "Fuel_Price",
        "CPI",
        "Unemployment",
        "IsHoliday",
        "Year",
        "Month",
        "Week",
        "Quarter"
    ]
]

# Target
y = df["Weekly_Sales"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    random_state=42
)

print("Training XGBoost...")

model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)

rmse = np.sqrt(
    mean_squared_error(y_test, preds)
)

non_zero_mask = y_test != 0

mape = np.mean(
    np.abs(
        (y_test[non_zero_mask] - preds[non_zero_mask])
        / y_test[non_zero_mask]
    )
) * 100

print("\nXGBoost Results")
print("----------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE:", round(mape, 2), "%")


import joblib

model_path = (
    BASE_DIR /
    "models/xgboost_model.pkl"
)

joblib.dump(model, model_path)

print("\nModel Saved:")
print(model_path)

# Save Actual vs Predicted values for the Model Performance dashboard page
predictions_df = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": preds
})

predictions_path = BASE_DIR / "data/processed/predictions.csv"

predictions_df.to_csv(predictions_path, index=False)

print("\nPredictions Saved:")
print(predictions_path)