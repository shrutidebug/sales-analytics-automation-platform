-- ============================================================
-- Sales Analytics & Automation Platform
-- SQL Analysis Queries
-- ============================================================
-- Analytical queries used during project validation and reporting.
-- These queries assume the star schema created in schema.sql.
-- ============================================================


-- ============================================================
-- A. BASIC SALES ANALYSIS
-- ============================================================

-- 1. Overall Performance
-- Total transactions, units sold, sales amount and average
-- sales amount per transaction.

SELECT
    COUNT(*) AS total_transactions,
    SUM(quantity) AS total_units,
    SUM(sales_amount) AS total_sales,
    AVG(sales_amount) AS average_sales
FROM fact_sales;


-- 2. Monthly Sales
-- Total sales for each month.

SELECT
    d.year,
    d.month,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 3. Monthly Transaction Count

SELECT
    d.year,
    d.month,
    COUNT(*) AS total_transactions
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 4. Monthly Units Sold

SELECT
    d.year,
    d.month,
    SUM(f.quantity) AS total_units
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- ============================================================
-- B. REGION ANALYSIS
-- ============================================================

-- 5. Sales by Region
-- Transactions, units sold and total sales.

SELECT
    r.region_name AS region,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS total_units,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_region r
    ON f.region_key = r.region_key
GROUP BY r.region_name
ORDER BY total_sales DESC;


-- 6. Region with Highest Total Sales

SELECT
    r.region_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_region r
    ON f.region_key = r.region_key
GROUP BY r.region_name
ORDER BY total_sales DESC
LIMIT 1;


-- 7. Region Contribution to Total Sales

SELECT
    r.region_name,
    ROUND(
        SUM(f.sales_amount) * 100.0
        / SUM(SUM(f.sales_amount)) OVER (),
        2
    ) AS sales_percent
FROM fact_sales f
JOIN dim_region r
    ON f.region_key = r.region_key
GROUP BY r.region_name
ORDER BY sales_percent DESC;


-- ============================================================
-- C. PRODUCT ANALYSIS
-- ============================================================

-- 8. Sales by Product

SELECT
    p.product_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_sales DESC;


-- 9. Best-Selling Product by Revenue

SELECT
    p.product_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 1;


-- 10. Most Sold Product by Quantity

SELECT
    p.product_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY units_sold DESC
LIMIT 1;


-- 11. Product Revenue Contribution

SELECT
    p.product_name,
    ROUND(
        SUM(f.sales_amount) * 100.0
        / SUM(SUM(f.sales_amount)) OVER (),
        2
    ) AS product_percent
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY product_percent DESC;


-- ============================================================
-- D. CUSTOMER ANALYSIS
-- ============================================================

-- 12. Sales by Customer

SELECT
    c.customer_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_name
ORDER BY total_sales DESC;


-- 13. Top 10 Customers by Sales

SELECT
    c.customer_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_name
ORDER BY total_sales DESC
LIMIT 10;


-- 14. Highest-Value Customer

SELECT
    c.customer_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_name
ORDER BY total_sales DESC
LIMIT 1;


-- 15. Customer Purchase Frequency
-- Top 10 customers by number of transactions.

SELECT
    c.customer_name,
    COUNT(*) AS transactions,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_name
ORDER BY transactions DESC
LIMIT 10;


-- ============================================================
-- E. TIME ANALYSIS
-- ============================================================

-- 16. Daily Sales

SELECT
    d.year,
    d.month,
    d.day,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.day
ORDER BY d.year, d.month, d.day;


-- 17. Best Sales Day

SELECT
    d.year,
    d.month,
    d.day,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.day
ORDER BY total_sales DESC
LIMIT 1;


-- 18. Best Sales Month

SELECT
    d.year,
    d.month,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY total_sales DESC
LIMIT 1;


-- 19. Month-over-Month Sales Growth

WITH monthly_sales AS (
    SELECT
        d.year,
        d.month,
        d.month_name,
        SUM(f.sales_amount) AS current_sales
    FROM fact_sales f
    JOIN dim_date d
        ON f.date_key = d.date_key
    GROUP BY d.year, d.month, d.month_name
)
SELECT
    year,
    month_name,
    current_sales,
    LAG(current_sales) OVER (
        PARTITION BY year
        ORDER BY month
    ) AS previous_sales,
    ROUND(
        (
            current_sales
            - LAG(current_sales) OVER (
                PARTITION BY year
                ORDER BY month
            )
        ) * 100.0
        / NULLIF(
            LAG(current_sales) OVER (
                PARTITION BY year
                ORDER BY month
            ),
            0
        ),
        2
    ) AS growth_percent
FROM monthly_sales
ORDER BY year, month;


-- ============================================================
-- F. COMBINED ANALYSIS
-- ============================================================

-- 20. Product by Region

SELECT
    p.product_name,
    r.region_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
JOIN dim_region r
    ON f.region_key = r.region_key
GROUP BY p.product_name, r.region_name
ORDER BY total_sales;


-- 21. Product Performance by Month

SELECT
    p.product_name,
    d.month_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY p.product_name, d.month, d.month_name
ORDER BY total_sales;


-- 22. Region Performance by Month

SELECT
    r.region_name,
    d.month_name,
    SUM(f.sales_amount) AS total_sales
FROM fact_sales f
JOIN dim_region r
    ON f.region_key = r.region_key
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY r.region_name, d.month, d.month_name
ORDER BY total_sales;


-- 23. Top Product in Each Region

WITH product_region_sales AS (
    SELECT
        p.product_name,
        r.region_name,
        SUM(f.sales_amount) AS total_sales
    FROM fact_sales f
    JOIN dim_product p
        ON f.product_key = p.product_key
    JOIN dim_region r
        ON f.region_key = r.region_key
    GROUP BY p.product_name, r.region_name
),
ranked_products AS (
    SELECT
        product_name,
        region_name,
        total_sales,
        RANK() OVER (
            PARTITION BY region_name
            ORDER BY total_sales DESC
        ) AS sales_rank
    FROM product_region_sales
)
SELECT
    product_name,
    region_name,
    total_sales
FROM ranked_products
WHERE sales_rank = 1
ORDER BY region_name;


-- 24. Top Customer in Each Region

WITH customer_region_sales AS (
    SELECT
        c.customer_name,
        r.region_name,
        SUM(f.sales_amount) AS total_sales
    FROM fact_sales f
    JOIN dim_customer c
        ON f.customer_key = c.customer_key
    JOIN dim_region r
        ON f.region_key = r.region_key
    GROUP BY c.customer_name, r.region_name
),
ranked_customers AS (
    SELECT
        customer_name,
        region_name,
        total_sales,
        RANK() OVER (
            PARTITION BY region_name
            ORDER BY total_sales DESC
        ) AS sales_rank
    FROM customer_region_sales
)
SELECT
    customer_name,
    region_name,
    total_sales
FROM ranked_customers
WHERE sales_rank = 1
ORDER BY region_name;


-- ============================================================
-- G. BUSINESS QUESTIONS
-- ============================================================

-- 25. Month with Highest Revenue

SELECT
    d.month_name,
    SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY revenue DESC
LIMIT 1;


-- 26. Region with Highest Revenue

SELECT
    r.region_name,
    SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_region r
    ON f.region_key = r.region_key
GROUP BY r.region_name
ORDER BY revenue DESC
LIMIT 1;


-- 27. Product with Highest Revenue

SELECT
    p.product_name,
    SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 1;


-- ============================================================
-- END OF ANALYSIS QUERIES
-- ============================================================
