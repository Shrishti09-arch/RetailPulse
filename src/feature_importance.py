from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(
    BASE_DIR /
    "models/xgboost_model.pkl"
)

features = [
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

importance = model.feature_importances_

imp_df = pd.DataFrame(
    {
        "Feature": features,
        "Importance": importance
    }
)

imp_df = imp_df.sort_values(
    "Importance",
    ascending=False
)

plt.figure(figsize=(10,6))

plt.barh(
    imp_df["Feature"],
    imp_df["Importance"]
)

plt.title(
    "Feature Importance"
)

plt.tight_layout()

plt.savefig(
    BASE_DIR /
    "images/feature_importance.png"
)

plt.show()