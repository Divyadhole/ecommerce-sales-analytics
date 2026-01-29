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

# Power BI inspired color palette
COLORS = {
    'primary': '#00B8AA',     # Teal (like Power BI demo)
    'secondary': '#0078D4',   # Microsoft Blue
    'chart1': '#00B8AA',      # Teal
    'chart2': '#8764B8',      # Purple
    'chart3': '#F18F01',      # Orange
    'chart4': '#CA5010',      # Red-Orange
    'chart5': '#038387',      # Dark Teal
    'neutral': '#605E5C',     # Gray
    'background': '#F3F2F1',  # Light Gray (Power BI style)
    'card_bg': '#FFFFFF',     # White
}

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
    LIMIT 10
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
    LIMIT 10
    """
    regional = pd.read_sql_query(regional_query, conn)
    
    # B2B vs B2C
    b2b_query = """
    SELECT 
        CASE WHEN b2b = 1 THEN 'B2B' ELSE 'B2C' END as type,
        COUNT(DISTINCT order_id) as orders,
        ROUND(SUM(amount), 2) as revenue
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
    GROUP BY type
    """
    b2b = pd.read_sql_query(b2b_query, conn)
    
    # Sales Channel
    channel_query = """
    SELECT 
        sales_channel,
        COUNT(DISTINCT order_id) as orders,
        ROUND(SUM(amount), 2) as revenue
    FROM sales
    WHERE status NOT LIKE '%Cancelled%'
    GROUP BY sales_channel
    ORDER BY revenue DESC
    """
    channels = pd.read_sql_query(channel_query, conn)
    
    # Order Status
    status_query = """
    SELECT 
        CASE 
            WHEN status LIKE '%Delivered%' THEN 'Delivered'
            WHEN status LIKE '%Shipped%' THEN 'Shipped'
            WHEN status LIKE '%Pending%' THEN 'Pending'
            WHEN status LIKE '%Cancelled%' THEN 'Cancelled'
            ELSE 'Other'
        END as status_group,
        COUNT(DISTINCT order_id) as orders
    FROM sales
    GROUP BY status_group
    ORDER BY orders DESC
    """
    statuses = pd.read_sql_query(status_query, conn)
    
    conn.close()
    
    return kpis, monthly, products, categories, regional, b2b, channels, statuses

def create_powerbi_dashboard():
    """Generate Power BI-style HTML dashboard."""
    
    print("Fetching data from database...")
    kpis, monthly, products, categories, regional, b2b, channels, statuses = get_data()
    
    # Format numbers
    total_revenue = kpis['total_revenue'].iloc[0]
    total_orders = kpis['total_orders'].iloc[0]
    total_units = kpis['total_units'].iloc[0]
    avg_order = kpis['avg_order_value'].iloc[0]
    
    # Create HTML structure with Power BI styling
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Sales Analytics | Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: {COLORS['background']};
            padding: 16px;
            color: #333;
        }}
        
        .dashboard-container {{
            max-width: 1800px;
            margin: 0 auto;
        }}
        
        .header {{
            background: {COLORS['card_bg']};
            padding: 20px 24px;
            border-radius: 4px;
            box-shadow: 0 0.3px 0.9px rgba(0, 0, 0, 0.07), 0 1.6px 3.6px rgba(0, 0, 0, 0.1);
            margin-bottom: 16px;
        }}
        
        h1 {{
            color: #323130;
            font-size: 24px;
            font-weight: 600;
            margin: 0;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 16px;
        }}
        
        .kpi-tile {{
            background: {COLORS['card_bg']};
            border-radius: 4px;
            padding: 24px;
            box-shadow: 0 0.3px 0.9px rgba(0, 0, 0, 0.07), 0 1.6px 3.6px rgba(0, 0, 0, 0.1);
            border-left: 3px solid {COLORS['primary']};
        }}
        
        .kpi-tile:nth-child(2) {{ border-left-color: {COLORS['secondary']}; }}
        .kpi-tile:nth-child(3) {{ border-left-color: {COLORS['chart2']}; }}
        .kpi-tile:nth-child(4) {{ border-left-color: {COLORS['chart3']}; }}
        
        .kpi-label {{
            font-size: 12px;
            color: {COLORS['neutral']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            font-weight: 600;
        }}
        
        .kpi-value {{
            font-size: 42px;
            font-weight: 600;
            color: #201F1E;
            line-height: 1;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 16px;
        }}
        
        .chart-tile {{
            background: {COLORS['card_bg']};
            border-radius: 4px;
            padding: 20px;
            box-shadow: 0 0.3px 0.9px rgba(0, 0, 0, 0.07), 0 1.6px 3.6px rgba(0, 0, 0, 0.1);
        }}
        
        .chart-tile.full-width {{
            grid-column: span 12;
        }}
        
        .chart-tile.half-width {{
            grid-column: span 6;
        }}
        
        .chart-tile.third-width {{
            grid-column: span 4;
        }}
        
        .chart-title {{
            font-size: 14px;
            color: #323130;
            margin-bottom: 12px;
            font-weight: 600;
        }}
        
        .footer {{
            text-align: center;
            color: {COLORS['neutral']};
            margin-top: 24px;
            padding: 16px;
            font-size: 11px;
        }}
        
        @media (max-width: 1400px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            .chart-tile.half-width,
            .chart-tile.third-width {{
                grid-column: span 12;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Header -->
        <div class="header">
            <h1>E-Commerce Sales Analytics Dashboard</h1>
        </div>
        
        <!-- KPI Tiles -->
        <div class="kpi-grid">
            <div class="kpi-tile">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹{total_revenue/1000000:.1f}M</div>
            </div>
            <div class="kpi-tile">
                <div class="kpi-label">Total Orders</div>
                <div class="kpi-value">{total_orders/1000:.0f}K</div>
            </div>
            <div class="kpi-tile">
                <div class="kpi-label">Units Sold</div>
                <div class="kpi-value">{total_units/1000:.0f}K</div>
            </div>
            <div class="kpi-tile">
                <div class="kpi-label">Avg Order Value</div>
                <div class="kpi-value">₹{avg_order:.0f}</div>
            </div>
        </div>
        
        <!-- Charts Grid -->
        <div class="charts-grid">
            <!-- Monthly Sales Trend - Full Width -->
            <div class="chart-tile full-width">
                <div class="chart-title">Monthly Sales Trend</div>
                <div id="monthly-chart"></div>
            </div>
            
            <!-- Category Performance - Half Width -->
            <div class="chart-tile half-width">
                <div class="chart-title">Revenue by Category</div>
                <div id="category-chart"></div>
            </div>
            
            <!-- Top Products - Half Width -->
            <div class="chart-tile half-width">
                <div class="chart-title">Top 10 Products by Revenue</div>
                <div id="products-chart"></div>
            </div>
            
            <!-- Regional Performance - Half Width -->
            <div class="chart-tile half-width">
                <div class="chart-title">Top 10 States by Revenue</div>
                <div id="regional-chart"></div>
            </div>
            
            <!-- B2B vs B2C - Third Width -->
            <div class="chart-tile third-width">
                <div class="chart-title">B2B vs B2C</div>
                <div id="b2b-chart"></div>
            </div>
            
            <!-- Sales Channel - Third Width -->
            <div class="chart-tile third-width">
                <div class="chart-title">Sales Channels</div>
                <div id="channel-chart"></div>
            </div>
            
            <!-- Order Status - Third Width -->
            <div class="chart-tile third-width">
                <div class="chart-title">Order Status</div>
                <div id="status-chart"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>E-Commerce Sales Analytics | Data from 2022 | {total_orders:,} orders analyzed</p>
        </div>
    </div>
    
    <script>
"""
    
    # Chart 1: Monthly Sales Trend (Power BI teal area chart style)
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=monthly['month'],
        y=monthly['revenue'],
        mode='lines',
        name='Revenue',
        line=dict(color=COLORS['primary'], width=2),
        fill='tozeroy',
        fillcolor=f"rgba(0, 184, 170, 0.2)",
        hovertemplate='<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>'
    ))
    fig_monthly.update_layout(
        xaxis_title='',
        yaxis_title='Revenue (₹)',
        hovermode='x unified',
        template='plotly_white',
        height=320,
        margin=dict(l=50, r=20, t=10, b=40),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EDEBE9')
    )
    
    # Chart 2: Category Performance (Horizontal Bar - Power BI style)
    fig_category = go.Figure()
    fig_category.add_trace(go.Bar(
        y=categories['category'],
        x=categories['revenue'],
        orientation='h',
        marker=dict(color=COLORS['primary']),
        hovertemplate='<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>'
    ))
    fig_category.update_layout(
        xaxis_title='',
        yaxis_title='',
        template='plotly_white',
        height=320,
        margin=dict(l=100, r=20, t=10, b=40),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#EDEBE9'),
        yaxis=dict(autorange='reversed', showgrid=False)
    )
    
    # Chart 3: Top Products (Horizontal Bar)
    products['product'] = products['category'] + ' - ' + products['style'].str[:12]
    fig_products = go.Figure()
    fig_products.add_trace(go.Bar(
        y=products['product'].head(8),
        x=products['revenue'].head(8),
        orientation='h',
        marker=dict(color=COLORS['secondary']),
        hovertemplate='<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>'
    ))
    fig_products.update_layout(
        xaxis_title='',
        yaxis_title='',
        template='plotly_white',
        height=320,
        margin=dict(l=140, r=20, t=10, b=40),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#EDEBE9'),
        yaxis=dict(autorange='reversed', showgrid=False)
    )
    
    # Chart 4: Regional Performance (Column Chart - Power BI style)
    fig_regional = go.Figure()
    fig_regional.add_trace(go.Bar(
        x=regional['state'].head(8),
        y=regional['revenue'].head(8),
        marker=dict(color=COLORS['chart3']),
        hovertemplate='<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>'
    ))
    fig_regional.update_layout(
        xaxis_title='',
        yaxis_title='Revenue (₹)',
        template='plotly_white',
        height=320,
        margin=dict(l=50, r=20, t=10, b=60),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor='#EDEBE9')
    )
    
    # Chart 5: B2B vs B2C (Donut Chart)
    fig_b2b = go.Figure()
    fig_b2b.add_trace(go.Pie(
        labels=b2b['type'],
        values=b2b['revenue'],
        hole=0.5,
        marker=dict(colors=[COLORS['primary'], COLORS['chart2']]),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>'
    ))
    fig_b2b.update_layout(
        template='plotly_white',
        height=280,
        margin=dict(l=20, r=20, t=10, b=20),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Chart 6: Sales Channel (Donut Chart)
    fig_channel = go.Figure()
    fig_channel.add_trace(go.Pie(
        labels=channels['sales_channel'],
        values=channels['revenue'],
        hole=0.5,
        marker=dict(colors=[COLORS['secondary'], COLORS['chart2'], COLORS['chart3']]),
        textinfo='label+percent',
        textfont=dict(size=11),
        hovertemplate='<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>'
    ))
    fig_channel.update_layout(
        template='plotly_white',
        height=280,
        margin=dict(l=20, r=20, t=10, b=20),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Chart 7: Order Status (Donut Chart)
    fig_status = go.Figure()
    fig_status.add_trace(go.Pie(
        labels=statuses['status_group'],
        values=statuses['orders'],
        hole=0.5,
        marker=dict(colors=[COLORS['primary'], COLORS['chart2'], COLORS['chart3'], COLORS['chart4'], COLORS['neutral']]),
        textinfo='label+percent',
        textfont=dict(size=11),
        hovertemplate='<b>%{label}</b><br>%{value:,} orders<extra></extra>'
    ))
    fig_status.update_layout(
        template='plotly_white',
        height=280,
        margin=dict(l=20, r=20, t=10, b=20),
        font=dict(family='Segoe UI', size=11, color='#605E5C'),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add all charts to HTML
    html_content += f"""
        // Chart 1: Monthly Trend
        var monthlyData = {fig_monthly.to_json()};
        Plotly.newPlot('monthly-chart', monthlyData.data, monthlyData.layout, {{responsive: true, displayModeBar: false}});
        
        // Chart 2: Category
        var categoryData = {fig_category.to_json()};
        Plotly.newPlot('category-chart', categoryData.data, categoryData.layout, {{responsive: true, displayModeBar: false}});
        
        // Chart 3: Products
        var productsData = {fig_products.to_json()};
        Plotly.newPlot('products-chart', productsData.data, productsData.layout, {{responsive: true, displayModeBar: false}});
        
        // Chart 4: Regional
        var regionalData = {fig_regional.to_json()};
        Plotly.newPlot('regional-chart', regionalData.data, regionalData.layout, {{responsive: true, displayModeBar: false}});
        
        // Chart 5: B2B
        var b2bData = {fig_b2b.to_json()};
        Plotly.newPlot('b2b-chart', b2bData.data, b2bData.layout, {{responsive: true, displayModeBar: false}});
        
        // Chart 6: Channel
        var channelData = {fig_channel.to_json()};
        Plotly.newPlot('channel-chart', channelData.data, channelData.layout, {{responsive: true, displayModeBar: false}});
        
        // Chart 7: Status
        var statusData = {fig_status.to_json()};
        Plotly.newPlot('status-chart', statusData.data, statusData.layout, {{responsive: true, displayModeBar: false}});
    </script>
</body>
</html>
"""
    
    # Write to file
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Power BI-style dashboard generated!")
    print(f"📊 Location: {OUTPUT_HTML}")
    print(f"🎨 Style: Clean Power BI theme with teal/blue colors")
    print(f"📈 Features: 4 KPI tiles + 7 interactive visualizations")

if __name__ == "__main__":
    create_powerbi_dashboard()
