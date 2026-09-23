import pandas as pd
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "ecommerce_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(INPUT_FILE)

df["visit_date"] = pd.to_datetime(df["visit_date"])


# =========================================================
# BUSINESS KPI ANALYSIS
# =========================================================

total_revenue = df["revenue"].sum()
total_sessions = len(df)
total_customers = df["customer_id"].nunique()
total_orders = df["purchased"].sum()

purchase_rate = df["purchased"].mean() * 100
cart_abandonment_rate = df["cart_abandoned"].mean() * 100
add_to_cart_rate = df["added_to_cart"].mean() * 100

purchased_df = df[df["purchased"] == 1]

average_order_value = purchased_df["revenue"].mean()


# =========================================================
# MONTHLY ANALYSIS
# =========================================================

monthly = (
    df.groupby(df["visit_date"].dt.to_period("M"))
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
        customers=("customer_id", "nunique"),
    )
    .reset_index()
)

monthly["month"] = monthly["visit_date"].astype(str)

monthly = monthly.drop(columns=["visit_date"])

monthly["conversion_rate"] = (
    monthly["orders"] / monthly["sessions"] * 100
)

highest_revenue_month = monthly.loc[
    monthly["revenue"].idxmax()
]

lowest_revenue_month = monthly.loc[
    monthly["revenue"].idxmin()
]


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

category = (
    df.groupby("product_category")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
        quantity=("quantity", "sum"),
    )
    .reset_index()
)

category["revenue_share"] = (
    category["revenue"] / total_revenue * 100
)

category["conversion_rate"] = (
    category["orders"] / category["sessions"] * 100
)

category = category.sort_values(
    "revenue",
    ascending=False
)


# =========================================================
# MARKETING ANALYSIS
# =========================================================

marketing = (
    df.groupby("marketing_channel")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
        customers=("customer_id", "nunique"),
    )
    .reset_index()
)

marketing["conversion_rate"] = (
    marketing["orders"] / marketing["sessions"] * 100
)

marketing["revenue_share"] = (
    marketing["revenue"] / total_revenue * 100
)

marketing = marketing.sort_values(
    "revenue",
    ascending=False
)


# =========================================================
# DEVICE ANALYSIS
# =========================================================

device = (
    df.groupby("device_type")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
    )
    .reset_index()
)

device["conversion_rate"] = (
    device["orders"] / device["sessions"] * 100
)

device["revenue_share"] = (
    device["revenue"] / total_revenue * 100
)


# =========================================================
# USER TYPE ANALYSIS
# =========================================================

user_type = (
    df.groupby("user_type")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
    )
    .reset_index()
)

user_type["conversion_rate"] = (
    user_type["orders"] / user_type["sessions"] * 100
)

user_type["revenue_share"] = (
    user_type["revenue"] / total_revenue * 100
)


# =========================================================
# CUSTOMER BEHAVIOR ANALYSIS
# =========================================================

behavior = (
    df.groupby("purchased")
    .agg(
        avg_pages_viewed=("pages_viewed", "mean"),
        avg_time_on_site=("time_on_site_sec", "mean"),
        avg_discount=("discount_percent", "mean"),
        avg_rating=("rating", "mean"),
        avg_quantity=("quantity", "mean"),
    )
    .reset_index()
)

# Difference between purchasers and non-purchasers

purchasers = behavior[behavior["purchased"] == 1].iloc[0]
non_purchasers = behavior[behavior["purchased"] == 0].iloc[0]

time_difference = (
    purchasers["avg_time_on_site"]
    - non_purchasers["avg_time_on_site"]
)

pages_difference = (
    purchasers["avg_pages_viewed"]
    - non_purchasers["avg_pages_viewed"]
)


# =========================================================
# CUSTOMER VALUE ANALYSIS
# =========================================================

customer_analysis = (
    df.groupby("customer_id")
    .agg(
        sessions=("session_id", "count"),
        orders=("purchased", "sum"),
        revenue=("revenue", "sum"),
        avg_order_value=("revenue", "mean"),
        avg_time_on_site=("time_on_site_sec", "mean"),
    )
    .reset_index()
)

customer_analysis = customer_analysis.sort_values(
    "revenue",
    ascending=False
)

top_customers = customer_analysis.head(20)


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

products = (
    df.groupby("product_id")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        quantity=("quantity", "sum"),
        sessions=("session_id", "count"),
    )
    .reset_index()
)

products["conversion_rate"] = (
    products["orders"] / products["sessions"] * 100
)

products = products.sort_values(
    "revenue",
    ascending=False
)

top_products = products.head(20)


# =========================================================
# SAVE ANALYSIS FILES
# =========================================================

monthly.to_csv(
    OUTPUT_DIR / "business_monthly_analysis.csv",
    index=False
)

category.to_csv(
    OUTPUT_DIR / "business_category_analysis.csv",
    index=False
)

marketing.to_csv(
    OUTPUT_DIR / "business_marketing_analysis.csv",
    index=False
)

device.to_csv(
    OUTPUT_DIR / "business_device_analysis.csv",
    index=False
)

user_type.to_csv(
    OUTPUT_DIR / "business_user_type_analysis.csv",
    index=False
)

behavior.to_csv(
    OUTPUT_DIR / "business_behavior_analysis.csv",
    index=False
)

customer_analysis.to_csv(
    OUTPUT_DIR / "customer_value_analysis.csv",
    index=False
)

top_products.to_csv(
    OUTPUT_DIR / "top_products_analysis.csv",
    index=False
)


# =========================================================
# PRINT BUSINESS FINDINGS
# =========================================================

print("\n")
print("=" * 70)
print("BUSINESS INTELLIGENCE ANALYSIS")
print("=" * 70)

print("\n--- EXECUTIVE KPIs ---")

print(f"Revenue: ₹{total_revenue:,.2f}")
print(f"Orders: {total_orders:,}")
print(f"Customers: {total_customers:,}")
print(f"Sessions: {total_sessions:,}")
print(f"Purchase Rate: {purchase_rate:.2f}%")
print(f"Add-to-Cart Rate: {add_to_cart_rate:.2f}%")
print(f"Cart Abandonment Rate: {cart_abandonment_rate:.2f}%")
print(f"Average Order Value: ₹{average_order_value:,.2f}")


print("\n--- MONTHLY PERFORMANCE ---")

print(
    f"Highest revenue month: "
    f"{highest_revenue_month['month']} "
    f"(₹{highest_revenue_month['revenue']:,.2f})"
)

print(
    f"Lowest revenue month: "
    f"{lowest_revenue_month['month']} "
    f"(₹{lowest_revenue_month['revenue']:,.2f})"
)


print("\n--- CATEGORY PERFORMANCE ---")

print(
    f"Highest revenue category ID: "
    f"{int(category.iloc[0]['product_category'])}"
)

print(
    f"Revenue: "
    f"₹{category.iloc[0]['revenue']:,.2f}"
)

print(
    f"Revenue share: "
    f"{category.iloc[0]['revenue_share']:.2f}%"
)


print("\n--- MARKETING PERFORMANCE ---")

best_marketing = marketing.loc[
    marketing["conversion_rate"].idxmax()
]

print(
    f"Highest conversion channel ID: "
    f"{int(best_marketing['marketing_channel'])}"
)

print(
    f"Conversion rate: "
    f"{best_marketing['conversion_rate']:.2f}%"
)


print("\n--- DEVICE PERFORMANCE ---")

best_device = device.loc[
    device["conversion_rate"].idxmax()
]

print(
    f"Highest conversion device ID: "
    f"{int(best_device['device_type'])}"
)

print(
    f"Conversion rate: "
    f"{best_device['conversion_rate']:.2f}%"
)


print("\n--- USER TYPE PERFORMANCE ---")

best_user_type = user_type.loc[
    user_type["conversion_rate"].idxmax()
]

print(
    f"Highest conversion user type ID: "
    f"{int(best_user_type['user_type'])}"
)

print(
    f"Conversion rate: "
    f"{best_user_type['conversion_rate']:.2f}%"
)


print("\n--- CUSTOMER BEHAVIOR ---")

print(
    f"Purchasers spend approximately "
    f"{time_difference:.2f} more seconds on site on average."
)

print(
    f"Purchasers view approximately "
    f"{pages_difference:.2f} more pages on average."
)


print("\n--- TOP CUSTOMER ---")

print(
    f"Customer ID: "
    f"{int(top_customers.iloc[0]['customer_id'])}"
)

print(
    f"Revenue: "
    f"₹{top_customers.iloc[0]['revenue']:,.2f}"
)


print("\n--- TOP PRODUCT ---")

print(
    f"Product ID: "
    f"{int(top_products.iloc[0]['product_id'])}"
)

print(
    f"Revenue: "
    f"₹{top_products.iloc[0]['revenue']:,.2f}"
)


print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETED")
print("=" * 70)