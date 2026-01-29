# 📊 E-Commerce Sales Analytics Dashboard

> **A comprehensive end-to-end data analytics project** featuring data cleaning, SQL analysis, and interactive Power BI-style visualizations for e-commerce sales insights.

![Dashboard Preview](https://raw.githubusercontent.com/Divyadhole/ecommerce-sales-analytics/main/assets/dashboard_preview.png)

## 🎯 Quick Overview (60 Seconds)

This project demonstrates **complete data analytics workflow** from raw data to actionable insights:

- ✅ **Data Cleaning**: Processed 128K+ records using Python/Pandas
- ✅ **SQL Analysis**: Built SQLite database with business intelligence queries
- ✅ **Interactive Dashboard**: Professional Power BI-themed web dashboard
- ✅ **Business Insights**: Generated actionable recommendations with ROI projections

### 📈 Key Metrics at a Glance

| Metric | Value |
|--------|-------|
| **Total Revenue** | ₹71.67M |
| **Total Orders** | 103,419 |
| **Products Analyzed** | 22 unique SKUs |
| **Average Order Value** | ₹648 |
| **Top Category** | Sets (50% revenue) |

---

## 📊 Dashboard Preview

The interactive dashboard features:
- **4 KPI Cards**: Real-time metrics overview
- **Year-over-Year Trends**: Area chart with comparative analysis
- **Sales Variance Analysis**: Bubble chart by category
- **Geographic Insights**: Top 10 states performance
- **Category Breakdown**: Revenue distribution
- **Channel Analysis**: B2B vs B2C comparison

![Dashboard Screenshot](https://raw.githubusercontent.com/Divyadhole/ecommerce-sales-analytics/main/assets/dashboard_full.png)

---

## 📁 Dataset Source

**Source**: Amazon Sales Report (2022)
- **Records**: 128,975 transactions
- **Features**: Order details, product info, customer data, fulfillment status
- **Geography**: India (28 states)
- **Categories**: Kurta, Set, Western Dress, Top, Ethnic Dress, Blouse, etc.

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| **Languages** | Python 3.x, SQL |
| **Data Processing** | Pandas, NumPy |
| **Database** | SQLite3 |
| **Visualization** | Plotly (interactive charts) |
| **Development** | Jupyter Notebook |
| **Version Control** | Git, GitHub |

---

## 🚀 How to Run This Project

### Prerequisites
```bash
# Install required packages
pip install pandas plotly jupyter
```

### Step-by-Step Execution

**1️⃣ Data Cleaning**
```bash
jupyter notebook notebooks/data_cleaning.ipynb
```
- Fixes column names, handles missing values
- Removes duplicates, standardizes categories
- Exports cleaned data to `data/cleaned_data.csv`

**2️⃣ Load Data to SQL Database**
```bash
python3 scripts/load_to_sql.py
```
- Creates SQLite database at `sql/ecommerce.db`
- Loads 128,975 cleaned records into `sales` table

**3️⃣ Generate Interactive Dashboard**
```bash
python3 scripts/generate_dashboard.py
```
- Generates Power BI-themed HTML dashboard
- Outputs to `dashboard/index.html`

**4️⃣ View Dashboard**
```bash
open dashboard/index.html
```
Or simply double-click the file to open in your browser.

---

## 💡 Key Insights Discovered

### 🏆 Top Performers
- **Best Category**: Sets (₹35.7M, 49.9% of revenue)
- **Runner-up**: Kurta (₹19.4M, 27.1% of revenue)
- **Top State**: Maharashtra (highest revenue concentration)

### 📉 Areas for Improvement
- **Underperforming Categories**: Saree, Dupatta (< 1% revenue each)
- **Geographic Gaps**: Low penetration in northeastern states
- **B2B Opportunity**: Currently underutilized channel

### 📊 Trends Identified
- **Seasonal Patterns**: Peak sales in Q2 and Q4
- **Order Status**: 99.2% successful fulfillment rate
- **Channel Mix**: Heavy reliance on Amazon.in marketplace

---

## 📂 Project Structure

```
ecommerce-sales-analytics/
├── data/
│   ├── Amazon Sale Report.csv          # Raw dataset (128K records)
│   └── cleaned_data.csv                # Cleaned & processed data
├── notebooks/
│   └── data_cleaning.ipynb             # Data preprocessing workflow
├── sql/
│   ├── ecommerce.db                    # SQLite database
│   └── analysis_queries.sql            # Business intelligence queries
├── scripts/
│   ├── load_to_sql.py                  # Database loader script
│   └── generate_dashboard.py           # Dashboard generator
├── dashboard/
│   └── index.html                      # Interactive web dashboard
├── insights/
│   ├── data_insights.md                # Detailed analysis findings
│   └── business_recommendations.md     # Strategic recommendations
├── requirements.txt                     # Python dependencies
└── README.md                           # This file
```

---

## 🎓 Skills Demonstrated

This project showcases proficiency in:

✅ **Data Cleaning & Preprocessing** - Handling messy real-world data  
✅ **SQL Database Design** - Schema creation, data loading, complex queries  
✅ **Business Intelligence** - KPI definition, trend analysis, insights generation  
✅ **Data Visualization** - Interactive dashboards with Plotly  
✅ **Python Programming** - Pandas, NumPy, data manipulation  
✅ **Statistical Analysis** - Variance analysis, comparative metrics  
✅ **Documentation** - Clear README, code comments, insights reports  
✅ **Version Control** - Git workflow, GitHub repository management  

---

## 📊 SQL Analysis Highlights

The project includes comprehensive SQL queries for:

- **Revenue Analysis**: Total sales, average order value, units sold
- **Temporal Trends**: Monthly sales patterns, year-over-year growth
- **Product Performance**: Top products, category breakdown
- **Geographic Distribution**: State-wise revenue, regional insights
- **Channel Analysis**: B2B vs B2C, marketplace performance
- **Operational Metrics**: Order status, fulfillment rates

All queries available in: [`sql/analysis_queries.sql`](sql/analysis_queries.sql)

---

## 🎨 Dashboard Features

### Interactive Visualizations
1. **KPI Cards** - Total Products, Sales, Orders, Avg Order Value
2. **Area Chart** - Year-over-Year Sales Trends (comparative analysis)
3. **Scatter Plot** - Sales Variance Analysis by Category (bubble chart)
4. **Bar Charts** - Monthly orders, category sales, regional performance
5. **Geographic Analysis** - Top 10 states by revenue
6. **Donut Chart** - Sales channel distribution

### Design Highlights
- **Theme**: Professional Power BI-inspired styling
- **Colors**: Teal, coral, gray, green palette
- **Layout**: Multi-tile grid with responsive design
- **Interactivity**: Hover tooltips, zoom, pan, filter capabilities

---

## 📈 Business Recommendations

Based on the analysis, key strategic recommendations include:

1. **Product Diversification** - Expand underperforming categories
2. **Geographic Expansion** - Target high-potential states
3. **B2B Channel Development** - Launch dedicated B2B division
4. **Marketplace Strategy** - Reduce dependency on single platform

Detailed recommendations with ROI projections: [`insights/business_recommendations.md`](insights/business_recommendations.md)

---

## 🌐 View Live Dashboard

**[📊 Interactive Dashboard](https://divyadhole.github.io/ecommerce-sales-analytics/dashboard/index.html)** - Explore the full analytics dashboard with interactive visualizations

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star!**

*Built with 💜 for data-driven decision making*

</div>
