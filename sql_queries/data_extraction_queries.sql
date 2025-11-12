-- SQL Queries for Data Extraction
-- These queries demonstrate common data extraction patterns for analytics

-- 1. Basic Sales Data Extraction
-- Extract all sales records from the last 30 days
SELECT 
    product_id,
    product_name,
    category,
    quantity,
    price,
    total_amount,
    sale_date,
    customer_id
FROM sales
WHERE sale_date >= DATE('now', '-30 days')
ORDER BY sale_date DESC;

-- 2. Aggregated Sales by Category
-- Get total sales and quantity by product category
SELECT 
    category,
    COUNT(*) as total_transactions,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value,
    MIN(sale_date) as first_sale,
    MAX(sale_date) as last_sale
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Top Performing Products
-- Identify top 10 products by revenue
SELECT 
    product_id,
    product_name,
    category,
    COUNT(*) as num_sales,
    SUM(quantity) as total_quantity_sold,
    SUM(total_amount) as total_revenue,
    AVG(price) as avg_price
FROM sales
GROUP BY product_id, product_name, category
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. Customer Purchase Analysis
-- Analyze customer purchase patterns
SELECT 
    customer_id,
    COUNT(DISTINCT product_id) as unique_products,
    COUNT(*) as total_purchases,
    SUM(total_amount) as total_spent,
    AVG(total_amount) as avg_purchase_value,
    MIN(sale_date) as first_purchase,
    MAX(sale_date) as last_purchase
FROM sales
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY total_spent DESC;

-- 5. Monthly Sales Trends
-- Track sales performance over time
SELECT 
    strftime('%Y-%m', sale_date) as month,
    COUNT(*) as num_transactions,
    SUM(quantity) as total_quantity,
    SUM(total_amount) as monthly_revenue,
    AVG(total_amount) as avg_transaction_value
FROM sales
GROUP BY strftime('%Y-%m', sale_date)
ORDER BY month;

-- 6. Sales with Missing Data Detection
-- Identify records that may need data cleaning
SELECT 
    product_id,
    product_name,
    category,
    quantity,
    price,
    total_amount,
    sale_date,
    CASE 
        WHEN product_name IS NULL OR product_name = '' THEN 'Missing Product Name'
        WHEN price IS NULL OR price <= 0 THEN 'Invalid Price'
        WHEN quantity IS NULL OR quantity <= 0 THEN 'Invalid Quantity'
        WHEN total_amount IS NULL THEN 'Missing Total Amount'
        ELSE 'Valid'
    END as data_quality_flag
FROM sales
WHERE product_name IS NULL OR product_name = ''
   OR price IS NULL OR price <= 0
   OR quantity IS NULL OR quantity <= 0
   OR total_amount IS NULL;

-- 7. Product Category Performance Comparison
-- Compare categories with statistical measures
SELECT 
    category,
    COUNT(*) as num_sales,
    MIN(total_amount) as min_sale,
    MAX(total_amount) as max_sale,
    AVG(total_amount) as mean_sale,
    SUM(total_amount) as total_revenue,
    SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM sales) as revenue_percentage
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;
