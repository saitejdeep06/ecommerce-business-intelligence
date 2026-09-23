import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# ============================================================
# LOAD ANALYSIS DATA
# ============================================================

monthly = pd.read_csv("outputs/business_monthly_analysis.csv")
category = pd.read_csv("outputs/business_category_analysis.csv")
marketing = pd.read_csv("outputs/business_marketing_analysis.csv")
device = pd.read_csv("outputs/business_device_analysis.csv")
user_type = pd.read_csv("outputs/business_user_type_analysis.csv")
behavior = pd.read_csv("outputs/business_behavior_analysis.csv")
products = pd.read_csv("outputs/top_products_analysis.csv")

# ============================================================
# 1. MONTHLY REVENUE TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly["month"],
    monthly["revenue"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Revenue Trend", fontsize=16, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 2. MONTHLY ORDERS TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly["month"],
    monthly["orders"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Orders Trend", fontsize=16, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/monthly_orders_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 3. CATEGORY REVENUE
# ============================================================

category_sorted = category.sort_values(
    "revenue",
    ascending=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=category_sorted,
    x="product_category",
    y="revenue"
)

plt.title(
    "Revenue by Product Category",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Product Category ID")
plt.ylabel("Revenue (₹)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/category_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 4. CATEGORY ORDERS
# ============================================================

category_orders = category.sort_values(
    "orders",
    ascending=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=category_orders,
    x="product_category",
    y="orders"
)

plt.title(
    "Orders by Product Category",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Product Category ID")
plt.ylabel("Orders")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/category_orders.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 5. MARKETING CHANNEL REVENUE
# ============================================================

marketing_sorted = marketing.sort_values(
    "revenue",
    ascending=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=marketing_sorted,
    x="marketing_channel",
    y="revenue"
)

plt.title(
    "Revenue by Marketing Channel",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Marketing Channel ID")
plt.ylabel("Revenue (₹)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/marketing_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 6. MARKETING CONVERSION
# ============================================================

marketing_conversion = marketing.sort_values(
    "conversion_rate",
    ascending=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=marketing_conversion,
    x="marketing_channel",
    y="conversion_rate"
)

plt.title(
    "Conversion Rate by Marketing Channel",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Marketing Channel ID")
plt.ylabel("Conversion Rate (%)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/marketing_conversion.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 7. DEVICE CONVERSION
# ============================================================

device_sorted = device.sort_values(
    "conversion_rate",
    ascending=False
)

plt.figure(figsize=(8, 6))

sns.barplot(
    data=device_sorted,
    x="device_type",
    y="conversion_rate"
)

plt.title(
    "Conversion Rate by Device",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Device Type ID")
plt.ylabel("Conversion Rate (%)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/device_conversion.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 8. USER TYPE CONVERSION
# ============================================================

user_sorted = user_type.sort_values(
    "conversion_rate",
    ascending=False
)

plt.figure(figsize=(8, 6))

sns.barplot(
    data=user_sorted,
    x="user_type",
    y="conversion_rate"
)

plt.title(
    "Conversion Rate by User Type",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("User Type ID")
plt.ylabel("Conversion Rate (%)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/user_type_conversion.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 9. CUSTOMER BEHAVIOR
# ============================================================

plt.figure(figsize=(8, 6))

sns.barplot(
    data=behavior,
    x="purchased",
    y="avg_time_on_site"
)

plt.title(
    "Average Time on Site: Purchasers vs Non-Purchasers",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Purchased")
plt.ylabel("Average Time on Site (seconds)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/customer_time_behavior.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 10. TOP PRODUCTS
# ============================================================

top_products = products.sort_values(
    "revenue",
    ascending=False
).head(10)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_products,
    x="product_id",
    y="revenue"
)

plt.title(
    "Top 10 Products by Revenue",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Product ID")
plt.ylabel("Revenue (₹)")

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/top_products_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# COMPLETION
# ============================================================

print()
print("=" * 70)
print("VISUALIZATION GENERATION COMPLETED")
print("=" * 70)
print()

print("Charts generated:")

for filename in sorted(os.listdir(OUTPUT_DIR)):
    if filename.endswith(".png"):
        print(f"✓ {filename}")

print()
print(f"Charts saved to: {OUTPUT_DIR}")
print("=" * 70)
