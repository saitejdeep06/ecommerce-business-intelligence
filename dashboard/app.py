import os
import pandas as pd
import streamlit as st
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEANED_DATA = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "ecommerce_cleaned.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CLEANED_DATA)

    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    monthly = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "business_monthly_analysis.csv"
        )
    )

    category = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "business_category_analysis.csv"
        )
    )

    marketing = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "business_marketing_analysis.csv"
        )
    )

    device = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "business_device_analysis.csv"
        )
    )

    user_type = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "business_user_type_analysis.csv"
        )
    )

    behavior = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "business_behavior_analysis.csv"
        )
    )

    products = pd.read_csv(
        os.path.join(
            OUTPUT_DIR,
            "top_products_analysis.csv"
        )
    )

    return (
        df,
        monthly,
        category,
        marketing,
        device,
        user_type,
        behavior,
        products
    )


(
    df,
    monthly,
    category,
    marketing,
    device,
    user_type,
    behavior,
    products
) = load_data()

# ============================================================
# CALCULATE KPIs
# ============================================================

total_revenue = df["revenue"].sum()

total_orders = int(
    df["purchased"].sum()
)

total_customers = df["customer_id"].nunique()

total_sessions = df["session_id"].nunique()

purchase_rate = (
    df["purchased"].mean() * 100
)

add_to_cart_rate = (
    df["added_to_cart"].mean() * 100
)

cart_abandonment_rate = (
    df["cart_abandoned"].mean() * 100
)

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 E-Commerce BI")

st.sidebar.markdown(
    """
    **AI-Powered E-Commerce Customer Behavior & Business Intelligence**
    
    Use the navigation below to explore business performance,
    customer behavior, risks and opportunities.
    """
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Sales & Product Analysis",
        "Customer & Risk Analysis",
        "Recommendations"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    f"Dataset: {len(df):,} sessions"
)

st.sidebar.caption(
    "Project: E-Commerce Business Intelligence"
)

# ============================================================
# HEADER
# ============================================================

st.title("🛍️ E-Commerce Business Intelligence Dashboard")

st.markdown(
    """
    **Turning customer and transaction data into actionable business insights**
    """
)

# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.header("📊 Executive Overview")

    st.markdown(
        "### Business Performance Snapshot"
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

    with col2:
        st.metric(
            "Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "Customers",
            f"{total_customers:,}"
        )

    with col4:
        st.metric(
            "Sessions",
            f"{total_sessions:,}"
        )

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "Purchase Rate",
            f"{purchase_rate:.2f}%"
        )

    with col6:
        st.metric(
            "Add-to-Cart Rate",
            f"{add_to_cart_rate:.2f}%"
        )

    with col7:
        st.metric(
            "Cart Abandonment",
            f"{cart_abandonment_rate:.2f}%"
        )

    with col8:
        st.metric(
            "Average Order Value",
            f"₹{average_order_value:,.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    st.subheader("📈 Monthly Revenue Trend")

    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # MONTHLY ORDERS
    # --------------------------------------------------------

    st.subheader("🛒 Monthly Orders")

    fig = px.bar(
        monthly,
        x="month",
        y="orders",
        title="Monthly Orders"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Orders"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # EXECUTIVE INSIGHTS
    # --------------------------------------------------------

    st.subheader("💡 Executive Insights")

    highest_month = monthly.loc[
        monthly["revenue"].idxmax()
    ]

    lowest_month = monthly.loc[
        monthly["revenue"].idxmin()
    ]

    st.info(
        f"""
        **Revenue:** ₹{total_revenue:,.2f}
        
        **Purchase rate:** {purchase_rate:.2f}%
        
        **Cart abandonment:** {cart_abandonment_rate:.2f}%
        
        **Highest revenue month:** {highest_month["month"]}
        with ₹{highest_month["revenue"]:,.2f}.
        
        **Lowest revenue month:** {lowest_month["month"]}
        with ₹{lowest_month["revenue"]:,.2f}.
        """
    )

# ============================================================
# PAGE 2 — SALES & PRODUCT ANALYSIS
# ============================================================

elif page == "Sales & Product Analysis":

    st.header("🛒 Sales & Product Analysis")

    # --------------------------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------------------------

    st.subheader("Product Category Performance")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            category.sort_values(
                "revenue",
                ascending=False
            ),
            x="product_category",
            y="revenue",
            title="Revenue by Product Category",
            labels={
                "product_category": "Category ID",
                "revenue": "Revenue (₹)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            category.sort_values(
                "orders",
                ascending=False
            ),
            x="product_category",
            y="orders",
            title="Orders by Product Category",
            labels={
                "product_category": "Category ID",
                "orders": "Orders"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # CATEGORY TABLE
    # --------------------------------------------------------

    st.subheader("Category Performance Table")

    category_display = category.copy()

    st.dataframe(
        category_display,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # MARKETING ANALYSIS
    # --------------------------------------------------------

    st.subheader("📣 Marketing Channel Performance")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            marketing.sort_values(
                "revenue",
                ascending=False
            ),
            x="marketing_channel",
            y="revenue",
            title="Revenue by Marketing Channel",
            labels={
                "marketing_channel": "Channel ID",
                "revenue": "Revenue (₹)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            marketing.sort_values(
                "conversion_rate",
                ascending=False
            ),
            x="marketing_channel",
            y="conversion_rate",
            title="Conversion Rate by Marketing Channel",
            labels={
                "marketing_channel": "Channel ID",
                "conversion_rate": "Conversion Rate (%)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    st.subheader("🏆 Top Products by Revenue")

    top_products = (
        products
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_products,
        x="product_id",
        y="revenue",
        title="Top 10 Products by Revenue",
        labels={
            "product_id": "Product ID",
            "revenue": "Revenue (₹)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# PAGE 3 — CUSTOMER & RISK ANALYSIS
# ============================================================

elif page == "Customer & Risk Analysis":

    st.header("👥 Customer & Risk Analysis")

    # --------------------------------------------------------
    # USER TYPE
    # --------------------------------------------------------

    st.subheader("User Type Conversion")

    fig = px.bar(
        user_type.sort_values(
            "conversion_rate",
            ascending=False
        ),
        x="user_type",
        y="conversion_rate",
        title="Conversion Rate by User Type",
        labels={
            "user_type": "User Type ID",
            "conversion_rate": "Conversion Rate (%)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    st.subheader("Device Conversion")

    fig = px.bar(
        device.sort_values(
            "conversion_rate",
            ascending=False
        ),
        x="device_type",
        y="conversion_rate",
        title="Conversion Rate by Device",
        labels={
            "device_type": "Device Type ID",
            "conversion_rate": "Conversion Rate (%)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # CUSTOMER BEHAVIOR
    # --------------------------------------------------------

    st.subheader("Customer Behavior")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            behavior,
            x="purchased",
            y="avg_time_on_site",
            title="Average Time on Site",
            labels={
                "purchased": "Purchased",
                "avg_time_on_site": "Average Time (seconds)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            behavior,
            x="purchased",
            y="avg_pages_viewed",
            title="Average Pages Viewed",
            labels={
                "purchased": "Purchased",
                "avg_pages_viewed": "Average Pages"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # RISK INDICATORS
    # --------------------------------------------------------

    st.subheader("⚠️ Risk Indicators")

    risk1, risk2, risk3 = st.columns(3)

    with risk1:

        st.metric(
            "Cart Abandonment",
            f"{cart_abandonment_rate:.2f}%"
        )

        st.caption(
            "Share of sessions marked as cart abandoned."
        )

    with risk2:

        st.metric(
            "Non-Purchase Sessions",
            f"{(1 - purchase_rate / 100) * 100:.2f}%"
        )

        st.caption(
            "Sessions that did not result in a purchase."
        )

    with risk3:

        st.metric(
            "Add-to-Cart Rate",
            f"{add_to_cart_rate:.2f}%"
        )

        st.caption(
            "Sessions where products were added to cart."
        )

    st.warning(
        """
        The 42.00% cart-abandonment rate is an important area
        for further investigation. The dataset shows the behavior,
        but it does not by itself establish the cause of abandonment.
        """
    )

# ============================================================
# PAGE 4 — RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":

    st.header("💡 Business Recommendations")

    st.markdown(
        """
        These recommendations are derived from the observed
        patterns in the dataset. They should be treated as
        business hypotheses to test rather than claims of causation.
        """
    )

    # --------------------------------------------------------
    # RECOMMENDATION 1
    # --------------------------------------------------------

    st.subheader("1. Investigate Cart Abandonment")

    st.write(
        f"""
        The dataset shows a cart-abandonment rate of
        **{cart_abandonment_rate:.2f}%**.
        
        The next business analysis should examine where abandonment
        is concentrated, such as by device, marketing channel,
        product category, or customer segment.
        """
    )

    # --------------------------------------------------------
    # RECOMMENDATION 2
    # --------------------------------------------------------

    st.subheader("2. Study High-Converting Marketing Channels")

    best_channel = marketing.loc[
        marketing["conversion_rate"].idxmax()
    ]

    st.write(
        f"""
        Marketing channel ID **{best_channel["marketing_channel"]}**
        has the highest observed conversion rate of
        **{best_channel["conversion_rate"]:.2f}%** in this dataset.
        
        The business could investigate what characteristics of
        this channel are associated with its observed performance
        before deciding whether to scale investment.
        """
    )

    # --------------------------------------------------------
    # RECOMMENDATION 3
    # --------------------------------------------------------

    st.subheader("3. Investigate High-Value Product Categories")

    best_category = category.loc[
        category["revenue"].idxmax()
    ]

    st.write(
        f"""
        Product category ID **{best_category["product_category"]}**
        generated the highest observed revenue:
        **₹{best_category["revenue"]:,.2f}**.
        
        Further analysis can examine product-level performance,
        pricing, quantity and customer behavior within this category.
        """
    )

    # --------------------------------------------------------
    # RECOMMENDATION 4
    # --------------------------------------------------------

    st.subheader("4. Analyze Customer Engagement")

    purchaser = behavior[
        behavior["purchased"] == 1
    ]

    non_purchaser = behavior[
        behavior["purchased"] == 0
    ]

    if not purchaser.empty and not non_purchaser.empty:

        purchaser_time = purchaser[
            "avg_time_on_site"
        ].iloc[0]

        non_purchaser_time = non_purchaser[
            "avg_time_on_site"
        ].iloc[0]

        difference = (
            purchaser_time -
            non_purchaser_time
        )

        st.write(
            f"""
            Purchasers spent approximately **{difference:.2f} seconds
            more on site on average than non-purchasers.
            
            This descriptive relationship can be investigated further
            to determine whether engagement-related interventions
            are associated with conversion changes.
            """
        )

    # --------------------------------------------------------
    # ACTION PLAN
    # --------------------------------------------------------

    st.subheader("🎯 Suggested Analysis Roadmap")

    st.markdown(
        """
        **Immediate analysis**
        
        - Investigate cart-abandonment patterns.
        - Examine marketing-channel performance.
        - Analyze high-revenue categories.
        
        **Next-stage analysis**
        
        - Segment customers.
        - Analyze repeat customer behavior.
        - Investigate product-level performance.
        - Compare conversion across devices.
        
        **Future enhancement**
        
        - Build a machine-learning model to predict purchase
          probability.
        - Add customer segmentation.
        - Add automated business alerts.
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Business Intelligence Project | "
    "Python • Pandas • Plotly • Streamlit"
)