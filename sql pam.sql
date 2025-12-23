CREATE VIEW v_sales_data AS
WITH cte_sales AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.sales_channel_id,
        o.total_amount,
        o.order_date,
        REPLACE(c.category_name, ' ', '-') AS category_name,  -- Заменяем пробелы на дефисы
        REPLACE(s.season_name, ' ', '-') AS season_name,  -- Заменяем пробелы на дефисы
        CASE
            WHEN o.total_amount > 1000 THEN 'High'
            WHEN o.total_amount BETWEEN 500 AND 1000 THEN 'Medium'
            ELSE 'Low'
        END AS order_size,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS rn
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN sales_channels s ON o.sales_channel_id = s.sales_channel_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '2 weeks'
)
SELECT DISTINCT
    customer_id,
    category_name || '|' || season_name AS category_season,  -- Конкатенация через палочку
    total_amount,
    order_id,
    order_size,
    rn
FROM cte_sales

UNION ALL

SELECT DISTINCT
    o.customer_id,
    REPLACE(c.category_name, ' ', '-') || '|' || REPLACE(s.season_name, ' ', '-') AS category_season,  -- Конкатенация через палочку
    o.total_amount,
    o.order_id,
    CASE
        WHEN o.total_amount > 1000 THEN 'High'
        WHEN o.total_amount BETWEEN 500 AND 1000 THEN 'Medium'
        ELSE 'Low'
    END AS order_size,
    ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS rn
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN sales_channels s ON o.sales_channel_id = s.sales_channel_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '1 month';  -- Example for another time range
