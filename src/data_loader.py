from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

train_path = BASE_DIR / "data" / "raw" / "train.csv"
features_path = BASE_DIR / "data" / "raw" / "features.csv"
stores_path = BASE_DIR / "data" / "raw" / "stores.csv"

print("Looking for:", train_path)

train = pd.read_csv(train_path)
features = pd.read_csv(features_path)
stores = pd.read_csv(stores_path)

print("Train Shape:", train.shape)
print("Features Shape:", features.shape)
print("Stores Shape:", stores.shape)