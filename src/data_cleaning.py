import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "dataset" / "Ecommerce.csv"
OUTPUT_DIR = BASE_DIR / "data" / "cleaned"
OUTPUT_FILE = OUTPUT_DIR / "ecommerce_cleaned.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")


# ---------------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------------

df.columns = df.columns.str.strip()


# ---------------------------------------------------------
# REMOVE DUPLICATE ROWS
# ---------------------------------------------------------

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

df = df.drop_duplicates()


# ---------------------------------------------------------
# CONVERT DATE
# ---------------------------------------------------------

df["visit_date"] = pd.to_datetime(
    df["visit_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

invalid_dates = df["visit_date"].isna().sum()

print(f"Invalid dates after conversion: {invalid_dates}")


# ---------------------------------------------------------
# NUMERIC COLUMNS
# ---------------------------------------------------------

numeric_columns = [
    "customer_id",
    "session_id",
    "device_type",
    "user_type",
    "marketing_channel",
    "product_id",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "purchased",
    "cart_abandoned",
    "rating",
    "review_text",
    "review_helpful_votes",
    "payment_method",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "revenue_normalized",
    "location",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# ---------------------------------------------------------
# BASIC VALIDATION
# ---------------------------------------------------------

print("\nChecking missing values...")

missing_values = df.isnull().sum()

print(missing_values[missing_values > 0])


# ---------------------------------------------------------
# VALIDATE IMPORTANT RANGES
# ---------------------------------------------------------

print("\nChecking important value ranges...")

checks = {
    "unit_price < 0": (df["unit_price"] < 0).sum(),
    "quantity <= 0": (df["quantity"] <= 0).sum(),
    "discount_percent < 0": (df["discount_percent"] < 0).sum(),
    "discount_percent > 100": (df["discount_percent"] > 100).sum(),
    "revenue < 0": (df["revenue"] < 0).sum(),
    "pages_viewed <= 0": (df["pages_viewed"] <= 0).sum(),
    "time_on_site_sec < 0": (df["time_on_site_sec"] < 0).sum(),
    "rating < 1": (df["rating"] < 1).sum(),
    "rating > 5": (df["rating"] > 5).sum(),
}

for check, count in checks.items():
    print(f"{check}: {count}")


# ---------------------------------------------------------
# SAVE CLEANED DATASET
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaning completed successfully.")

print(f"Final rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")
print(f"Saved to: {OUTPUT_FILE}")