import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SQL_DIR = os.path.join(PROJECT_ROOT, 'sql')
DB_FILE = os.path.join(SQL_DIR, 'ecommerce.db')
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, 'dashboard')
OUTPUT_HTML = os.path.join(DASHBOARD_DIR, 'index.html')

# Create dashboard directory if it doesn't exist
os.makedirs(DASHBOARD_DIR, exist_ok=True)

def get_data():
    """Connect to database and fetch all necessary data."""
    conn = sqlite3.connect(DB_FILE)
    
    # KPI Data
    kpi_query = """
    SELECT 
        COUNT(DISTINCT order_id) as total_orders,
        SUM(qty) as total_units,
        ROUND(SUM(amount), 2) as total_revenue,
        ROUND(AVG(amount), 2) as avg_order_value
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
    """
    kpis = pd.read_sql_query(kpi_query, conn)
    
    # Monthly Trend
    monthly_query = """
    SELECT 
        strftime('%Y-%m', date) as month,
        COUNT(DISTINCT order_id) as orders,
        SUM(qty) as units,
        ROUND(SUM(amount), 2) as revenue
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
    GROUP BY month
    ORDER BY month
    """
    monthly = pd.read_sql_query(monthly_query, conn)
    
    # Top Products
    products_query = """
    SELECT 
        category,
        style,
        SUM(qty) as units_sold,
        ROUND(SUM(amount), 2) as revenue
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
    GROUP BY category, style
    ORDER BY revenue DESC
    LIMIT 15
    """
    products = pd.read_sql_query(products_query, conn)
    
    # Category Performance
    category_query = """
    SELECT 
        category,
        COUNT(DISTINCT order_id) as orders,
        ROUND(SUM(amount), 2) as revenue
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
    GROUP BY category
    ORDER BY revenue DESC
    """
    categories = pd.read_sql_query(category_query, conn)
    
    # Regional Performance
    regional_query = """
    SELECT 
        "ship-state" as state,
        COUNT(DISTINCT order_id) as orders,
        ROUND(SUM(amount), 2) as revenue
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
        AND "ship-state" != 'Unknown'
    GROUP BY state
    ORDER BY revenue DESC
    LIMIT 15
    """
    regional = pd.read_sql_query(regional_query, conn)
    
    conn.close()
    
    return kpis, monthly, products, categories, regional

def create_dashboard():
    """Generate interactive HTML dashboard."""
    
    print("Fetching data from database...")
    kpis, monthly, products, categories, regional = get_data()
    
    # Create HTML structure
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Sales Analytics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .kpi-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .kpi-label {{
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .kpi-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .chart-title {{
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 E-Commerce Sales Analytics Dashboard</h1>
        
        <!-- KPI Cards -->
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹{kpis['total_revenue'].iloc[0]:,.0f}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Orders</div>
                <div class="kpi-value">{kpis['total_orders'].iloc[0]:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Units Sold</div>
                <div class="kpi-value">{kpis['total_units'].iloc[0]:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Order Value</div>
                <div class="kpi-value">₹{kpis['avg_order_value'].iloc[0]:,.0f}</div>
            </div>
        </div>
"""
    
    # Monthly Sales Trend Chart
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=monthly['month'],
        y=monthly['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    fig_monthly.update_layout(
        title='Monthly Sales Trend',
        xaxis_title='Month',
        yaxis_title='Revenue (₹)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    # Top Products Chart
    products['product'] = products['category'] + ' - ' + products['style']
    fig_products = go.Figure()
    fig_products.add_trace(go.Bar(
        x=products['revenue'].head(10),
        y=products['product'].head(10),
        orientation='h',
        marker=dict(
            color=products['revenue'].head(10),
            colorscale='Viridis',
            showscale=True
        )
    ))
    fig_products.update_layout(
        title='Top 10 Products by Revenue',
        xaxis_title='Revenue (₹)',
        yaxis_title='Product',
        template='plotly_white',
        height=500,
        yaxis=dict(autorange='reversed')
    )
    
    # Category Performance Pie Chart
    fig_category = go.Figure()
    fig_category.add_trace(go.Pie(
        labels=categories['category'],
        values=categories['revenue'],
        hole=0.4,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'])
    ))
    fig_category.update_layout(
        title='Revenue by Category',
        template='plotly_white',
        height=500
    )
    
    # Regional Performance Chart
    fig_regional = go.Figure()
    fig_regional.add_trace(go.Bar(
        x=regional['state'].head(10),
        y=regional['revenue'].head(10),
        marker=dict(
            color=regional['revenue'].head(10),
            colorscale='Blues',
            showscale=True
        )
    ))
    fig_regional.update_layout(
        title='Top 10 States by Revenue',
        xaxis_title='State',
        yaxis_title='Revenue (₹)',
        template='plotly_white',
        height=500
    )
    
    # Add charts to HTML
    html_content += f"""
        <div class="chart-container">
            <div id="monthly-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="products-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="category-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="regional-chart"></div>
        </div>
        
        <div class="footer">
            <p>Generated from {kpis['total_orders'].iloc[0]:,} orders | Last Updated: 2022</p>
        </div>
    </div>
    
    <script>
        {fig_monthly.to_html(div_id="monthly-chart", include_plotlyjs=False)}
        {fig_products.to_html(div_id="products-chart", include_plotlyjs=False)}
        {fig_category.to_html(div_id="category-chart", include_plotlyjs=False)}
        {fig_regional.to_html(div_id="regional-chart", include_plotlyjs=False)}
    </script>
</body>
</html>
"""
    
    # Write to file
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard generated successfully at: {OUTPUT_HTML}")
    print(f"📊 Open the file in your browser to view the interactive dashboard!")

if __name__ == "__main__":
    create_dashboard()
