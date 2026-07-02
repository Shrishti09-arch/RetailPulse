from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR /
    "data/processed/retailpulse_features.csv"
)

sales_by_store = (
    df.groupby("Store")["Weekly_Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

sales_by_store.head(20).plot(
    kind="bar"
)

plt.title(
    "Top 20 Stores by Sales"
)

plt.tight_layout()

plt.savefig(
    BASE_DIR /
    "images/top20stores.png"
)

plt.show()