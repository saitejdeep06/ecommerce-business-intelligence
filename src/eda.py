import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "ecommerce_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["visit_date"] = pd.to_datetime(df["visit_date"])


# ---------------------------------------------------------
# BASIC INFORMATION
# ---------------------------------------------------------

print("=" * 60)
print("E-COMMERCE BUSINESS INTELLIGENCE - EDA")
print("=" * 60)

print(f"\nRows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Unique Customers: {df['customer_id'].nunique():,}")
print(f"Unique Sessions: {df['session_id'].nunique():,}")


# ---------------------------------------------------------
# KEY PERFORMANCE INDICATORS
# ---------------------------------------------------------

total_revenue = df["revenue"].sum()

total_orders = df["purchased"].sum()

total_customers = df["customer_id"].nunique()

total_sessions = df["session_id"].nunique()

purchase_rate = df["purchased"].mean() * 100

cart_abandonment_rate = df["cart_abandoned"].mean() * 100

add_to_cart_rate = df["added_to_cart"].mean() * 100

average_order_value = (
    df.loc[df["purchased"] == 1, "revenue"].mean()
)

average_quantity = df["quantity"].mean()

average_discount = df["discount_percent"].mean()


print("\n" + "=" * 60)
print("KEY PERFORMANCE INDICATORS")
print("=" * 60)

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Total Sessions: {total_sessions:,}")
print(f"Purchase Rate: {purchase_rate:.2f}%")
print(f"Add-to-Cart Rate: {add_to_cart_rate:.2f}%")
print(f"Cart Abandonment Rate: {cart_abandonment_rate:.2f}%")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Average Quantity: {average_quantity:.2f}")
print(f"Average Discount: {average_discount:.2f}%")


# ---------------------------------------------------------
# MONTHLY PERFORMANCE
# ---------------------------------------------------------

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

monthly.to_csv(
    OUTPUT_DIR / "monthly_performance.csv",
    index=False
)

print("\n" + "=" * 60)
print("MONTHLY PERFORMANCE")
print("=" * 60)

print(monthly.to_string(index=False))


# ---------------------------------------------------------
# PRODUCT CATEGORY PERFORMANCE
# ---------------------------------------------------------

category_performance = (
    df.groupby("product_category")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        quantity=("quantity", "sum"),
        sessions=("session_id", "count"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

category_performance.to_csv(
    OUTPUT_DIR / "category_performance.csv",
    index=False
)

print("\n" + "=" * 60)
print("PRODUCT CATEGORY PERFORMANCE")
print("=" * 60)

print(category_performance.to_string(index=False))


# ---------------------------------------------------------
# MARKETING CHANNEL PERFORMANCE
# ---------------------------------------------------------

marketing_performance = (
    df.groupby("marketing_channel")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
        customers=("customer_id", "nunique"),
    )
    .reset_index()
)

marketing_performance["conversion_rate"] = (
    marketing_performance["orders"]
    / marketing_performance["sessions"]
    * 100
)

marketing_performance = marketing_performance.sort_values(
    "revenue",
    ascending=False
)

marketing_performance.to_csv(
    OUTPUT_DIR / "marketing_performance.csv",
    index=False
)

print("\n" + "=" * 60)
print("MARKETING CHANNEL PERFORMANCE")
print("=" * 60)

print(marketing_performance.to_string(index=False))


# ---------------------------------------------------------
# DEVICE PERFORMANCE
# ---------------------------------------------------------

device_performance = (
    df.groupby("device_type")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
    )
    .reset_index()
)

device_performance["conversion_rate"] = (
    device_performance["orders"]
    / device_performance["sessions"]
    * 100
)

device_performance.to_csv(
    OUTPUT_DIR / "device_performance.csv",
    index=False
)

print("\n" + "=" * 60)
print("DEVICE PERFORMANCE")
print("=" * 60)

print(device_performance.to_string(index=False))


# ---------------------------------------------------------
# USER TYPE PERFORMANCE
# ---------------------------------------------------------

user_type_performance = (
    df.groupby("user_type")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        sessions=("session_id", "count"),
    )
    .reset_index()
)

user_type_performance["conversion_rate"] = (
    user_type_performance["orders"]
    / user_type_performance["sessions"]
    * 100
)

user_type_performance.to_csv(
    OUTPUT_DIR / "user_type_performance.csv",
    index=False
)

print("\n" + "=" * 60)
print("USER TYPE PERFORMANCE")
print("=" * 60)

print(user_type_performance.to_string(index=False))


# ---------------------------------------------------------
# CUSTOMER BEHAVIOR
# ---------------------------------------------------------

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

behavior.to_csv(
    OUTPUT_DIR / "customer_behavior.csv",
    index=False
)

print("\n" + "=" * 60)
print("CUSTOMER BEHAVIOR")
print("=" * 60)

print(behavior.to_string(index=False))


# ---------------------------------------------------------
# TOP PRODUCTS
# ---------------------------------------------------------

top_products = (
    df.groupby("product_id")
    .agg(
        revenue=("revenue", "sum"),
        orders=("purchased", "sum"),
        quantity=("quantity", "sum"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(20)
)

top_products.to_csv(
    OUTPUT_DIR / "top_products.csv",
    index=False
)

print("\n" + "=" * 60)
print("TOP 20 PRODUCTS BY REVENUE")
print("=" * 60)

print(top_products.to_string(index=False))


# ---------------------------------------------------------
# SAVE KPI SUMMARY
# ---------------------------------------------------------

kpi_summary = pd.DataFrame(
    {
        "KPI": [
            "Total Revenue",
            "Total Orders",
            "Total Customers",
            "Total Sessions",
            "Purchase Rate",
            "Add-to-Cart Rate",
            "Cart Abandonment Rate",
            "Average Order Value",
            "Average Quantity",
            "Average Discount",
        ],
        "Value": [
            total_revenue,
            total_orders,
            total_customers,
            total_sessions,
            purchase_rate,
            add_to_cart_rate,
            cart_abandonment_rate,
            average_order_value,
            average_quantity,
            average_discount,
        ],
    }
)

kpi_summary.to_csv(
    OUTPUT_DIR / "kpi_summary.csv",
    index=False
)


print("\n" + "=" * 60)
print("EDA COMPLETED")
print("=" * 60)

print("\nOutput files created in:")
print(OUTPUT_DIR)