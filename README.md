# 📊 E-Commerce Sales Analytics

A comprehensive data analytics project analyzing e-commerce sales data through data cleaning, SQL analysis, and interactive visualizations.

## 🎯 Project Overview

This project demonstrates end-to-end data analytics workflow:
- **Data Cleaning**: Python/Pandas data preprocessing
- **SQL Analysis**: Business intelligence queries
- **Interactive Dashboard**: Web-based visualizations

## 📈 Key Insights

- **Total Revenue**: ₹71.67M from 103K+ orders
- **Best-Selling Category**: Sets (50% of revenue)
- **Average Order Value**: ₹648
- **Peak Sales Period**: Identified through monthly trend analysis

## 🗂️ Project Structure

```
ecommerce-sales-analytics/
├── data/
│   ├── Amazon Sale Report.csv          # Raw data
│   └── cleaned_data.csv                # Cleaned data
├── notebooks/
│   └── data_cleaning.ipynb             # Data cleaning process
├── sql/
│   ├── ecommerce.db                    # SQLite database
│   └── analysis_queries.sql            # Business queries
├── scripts/
│   ├── load_to_sql.py                  # Database loader
│   └── generate_dashboard.py           # Dashboard generator
├── dashboard/
│   └── index.html                      # Interactive dashboard
└── README.md
```

## 🚀 Getting Started

### Prerequisites

```bash
pip install pandas plotly
```

### Running the Project

1. **Data Cleaning**
   ```bash
   jupyter notebook notebooks/data_cleaning.ipynb
   ```

2. **Load Data to SQL**
   ```bash
   python3 scripts/load_to_sql.py
   ```

3. **Generate Dashboard**
   ```bash
   python3 scripts/generate_dashboard.py
   ```

4. **View Dashboard**
   Open `dashboard/index.html` in your browser

## 📊 Dashboard Features

- **KPI Cards**: Revenue, Orders, Units Sold, Avg Order Value
- **Monthly Sales Trend**: Interactive line chart
- **Top Products**: Best performers by revenue
- **Category Analysis**: Revenue distribution
- **Regional Performance**: Top states by sales

## 🔍 SQL Analysis

Key business queries available in `sql/analysis_queries.sql`:
- Total revenue analysis
- Monthly sales trends
- Top products by revenue
- Category performance
- Regional distribution
- B2B vs B2C comparison

## 📊 Data Pipeline

```
Raw Data → Cleaning → SQL Database → Analytics → Dashboard
```

1. **Cleaning** (`data_cleaning.ipynb`)
   - Fix column names
   - Handle missing values
   - Remove duplicates
   - Standardize categories
   - Convert dates

2. **SQL Analysis** (`analysis_queries.sql`)
   - Business intelligence queries
   - Aggregations and trends
   - Performance metrics

3. **Visualization** (`dashboard/index.html`)
   - Interactive charts
   - KPI cards
   - Regional maps

## 🛠️ Technologies Used

- **Python**: Data processing and analysis
- **Pandas**: Data manipulation
- **SQLite**: Database management
- **Plotly**: Interactive visualizations
- **Jupyter**: Development environment

## 📝 Key Findings

1. **Product Performance**
   - Sets category dominates with ₹35.7M (49.9%)
   - Kurtas second with ₹19.4M (27.1%)

2. **Regional Insights**
   - Top performing states identified
   - Urban centers drive majority of sales

3. **Sales Trends**
   - Monthly patterns reveal seasonality
   - Growth opportunities identified

## 🎓 Skills Demonstrated

- Data Cleaning & Preprocessing
- SQL Database Design
- Business Intelligence
- Data Visualization
- Python Programming
- Statistical Analysis

## 📧 Contact

**Divya Dhole**
- GitHub: [Divyadhole](https://github.com/Divyadhole)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 📄 License

This project is open source and available under the MIT License.

---

*Built with 💜 for data-driven decision making*
