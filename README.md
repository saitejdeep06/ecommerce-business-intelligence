# E-Commerce Business Intelligence Dashboard 

## 🚀 Live Dashboard

[Open Live Dashboard](https://ecommerce-business-intelligence-94sjxabpmtce6aq3qqye3f.streamlit.app/)

## Project Overview

This project is an E-Commerce Business Intelligence and Analytics solution that transforms raw e-commerce data into meaningful business insights.

The project follows the complete analytics workflow:

**Raw Data → Data Cleaning → Analysis → KPI Analysis → Business Insights → Recommendations**

The goal is to help an e-commerce business understand sales performance, customer behavior, product/category performance, device behavior, marketing performance, and conversion behavior.

---

## Business Problem

E-commerce businesses generate large amounts of customer, transaction, product, session, device, and marketing data.

Raw data does not directly answer important business questions such as:

- How much revenue is being generated?
- How many orders and customers are there?
- What is the average order value?
- Which categories perform well?
- Which devices generate the most activity?
- How effectively are visitors converted into customers?
- Where are customers dropping out of the purchase funnel?
- What actions can improve business performance?

This project analyzes the available data and converts the results into actionable business recommendations.

---

## Project Objectives

The main objectives are:

1. Clean and prepare the raw e-commerce dataset.
2. Calculate important business KPIs.
3. Analyze sales and order performance.
4. Understand customer behavior.
5. Analyze product and category performance.
6. Analyze device-level behavior.
7. Analyze marketing performance.
8. Analyze the conversion funnel.
9. Identify business opportunities and risks.
10. Provide data-driven recommendations.
11. Build an interactive Streamlit dashboard.

---

## Dataset

The project uses an e-commerce dataset containing information related to customers, sessions, orders, products, categories, devices, and purchasing behavior.

### Dataset Source

**Original Dataset Link:**  
Add the verified original dataset URL here.

> The original dataset source should be retained for transparency and reproducibility.

---

## Key Performance Indicators

| KPI | Value |
|---|---:|
| Total Revenue | ₹10,116,169.06 |
| Total Orders | 5,616 |
| Total Customers | 8,442 |
| Total Sessions | 25,000 |
| Purchase Rate | 22.46% |
| Add-to-Cart Rate | 64.47% |
| Abandonment Rate | 42.00% |
| Average Order Value | ₹1,801.31 |

These KPIs provide an overview of sales performance and customer conversion behavior.

---

## Data Cleaning

The project performs several data preparation activities:

- Loading the raw dataset
- Inspecting the dataset structure
- Checking missing values
- Cleaning data types
- Handling inconsistent records
- Creating calculated metrics
- Preparing the cleaned dataset for analysis

The cleaned dataset is stored at:

```text
data/cleaned/ecommerce_cleaned.csv