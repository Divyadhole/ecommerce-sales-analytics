-- =============================================
-- E-COMMERCE SALES ANALYTICS - SQL QUERIES
-- =============================================
-- Database: ecommerce.db
-- Table: sales
-- Purpose: Business intelligence queries for decision-making
-- =============================================

-- =============================================
-- 1. TOTAL REVENUE ANALYSIS
-- =============================================
-- Business Question: What is our total revenue from completed orders?
-- Insight: Overall business performance and revenue generation

SELECT 
    COUNT(DISTINCT order_id) as total_orders,
    SUM(qty) as total_units_sold,
    ROUND(SUM(amount), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM sales
WHERE status NOT LIKE '%Cancelled%';


-- =============================================
-- 2. MONTHLY SALES TREND
-- =============================================
-- Business Question: How are sales trending month over month?
-- Insight: Identify seasonality and growth patterns

SELECT 
    strftime('%Y-%m', date) as month,
    COUNT(DISTINCT order_id) as orders,
    SUM(qty) as units_sold,
    ROUND(SUM(amount), 2) as revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM sales
WHERE status NOT LIKE '%Cancelled%'
GROUP BY month
ORDER BY month DESC;


-- =============================================
-- 3. TOP PRODUCTS BY REVENUE
-- =============================================
-- Business Question: Which products drive the most revenue?
-- Insight: Focus inventory and marketing on high-performing products

SELECT 
    category,
    style,
    COUNT(DISTINCT order_id) as orders,
    SUM(qty) as units_sold,
    ROUND(SUM(amount), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_price
FROM sales
WHERE status NOT LIKE '%Cancelled%'
GROUP BY category, style
ORDER BY total_revenue DESC
LIMIT 20;


-- =============================================
-- 4. PROFIT BY CATEGORY
-- =============================================
-- Business Question: Which product categories perform best?
-- Insight: Strategic decisions on product portfolio

SELECT 
    category,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(qty) as total_units,
    ROUND(SUM(amount), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_revenue_per_order,
    ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM sales WHERE status NOT LIKE '%Cancelled%'), 2) as revenue_percentage
FROM sales
WHERE status NOT LIKE '%Cancelled%'
GROUP BY category
ORDER BY total_revenue DESC;


-- =============================================
-- 5. REGIONAL PERFORMANCE
-- =============================================
-- Business Question: Which regions generate the most sales?
-- Insight: Regional expansion and logistics optimization

SELECT 
    "ship-state" as state,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(qty) as total_units,
    ROUND(SUM(amount), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value,
    COUNT(DISTINCT "ship-city") as cities_served
FROM sales
WHERE status NOT LIKE '%Cancelled%'
    AND "ship-state" != 'Unknown'
GROUP BY state
ORDER BY total_revenue DESC
LIMIT 15;


-- =============================================
-- BONUS QUERIES
-- =============================================

-- Sales Channel Performance
SELECT 
    sales_channel,
    COUNT(DISTINCT order_id) as orders,
    ROUND(SUM(amount), 2) as revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM sales
WHERE status NOT LIKE '%Cancelled%'
GROUP BY sales_channel
ORDER BY revenue DESC;

-- B2B vs B2C Analysis
SELECT 
    CASE 
        WHEN b2b = 1 THEN 'B2B'
        ELSE 'B2C'
    END as business_type,
    COUNT(DISTINCT order_id) as orders,
    SUM(qty) as units,
    ROUND(SUM(amount), 2) as revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM sales
WHERE status NOT LIKE '%Cancelled%'
GROUP BY business_type;
