import pandas as pd
import joblib
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# =====================================================
# PATH CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset.csv"

MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(exist_ok=True)

# =====================================================
# LOAD DATASET
# =====================================================

try:

    df = pd.read_csv(DATASET_PATH)

except Exception as e:

    print(f"ERROR: Unable to load dataset.csv")
    print(str(e))
    exit()

# =====================================================
# VALIDATION
# =====================================================

required_columns = ["date", "visitors"]

for column in required_columns:

    if column not in df.columns:

        print(f"ERROR: Missing required column -> {column}")
        exit()

if len(df) < 5:

    print("ERROR: Dataset must contain at least 5 rows")
    exit()

# =====================================================
# DATA CLEANING
# =====================================================

df = df.copy()

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["visitors"] = pd.to_numeric(
    df["visitors"],
    errors="coerce"
)

df.dropna(inplace=True)

df.drop_duplicates(inplace=True)

df.sort_values(
    by="date",
    inplace=True
)

df.reset_index(
    drop=True,
    inplace=True
)

if len(df) < 5:

    print("ERROR: Not enough valid rows after cleaning")
    exit()

# =====================================================
# FEATURE ENGINEERING
# =====================================================

df["day"] = range(
    1,
    len(df) + 1
)

X = df[["day"]]

y = df["visitors"]

# =====================================================
# TRAIN LINEAR REGRESSION
# =====================================================

linear_model = LinearRegression()

linear_model.fit(
    X,
    y
)

# =====================================================
# TRAIN RANDOM FOREST
# =====================================================

rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf_model.fit(
    X,
    y
)

# =====================================================
# SAVE MODELS
# =====================================================

linear_model_path = (
    MODELS_DIR / "linear_model.pkl"
)

rf_model_path = (
    MODELS_DIR / "rf_model.pkl"
)

joblib.dump(
    linear_model,
    linear_model_path
)

joblib.dump(
    rf_model,
    rf_model_path
)

# =====================================================
# SUMMARY
# =====================================================

print("\n====================================")
print(" WEBSITE TRAFFIC FORECASTING")
print(" Model Training Completed")
print("====================================")
print(f"Dataset Rows     : {len(df)}")
print(f"Linear Model     : {linear_model_path}")
print(f"Random Forest    : {rf_model_path}")
print("====================================\n")