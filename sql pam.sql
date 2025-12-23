CREATE VIEW v_sales_data AS
WITH cte_sales AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.sales_channel_id,
        o.total_amount,
        o.order_date,
        c.category_name,
        s.season_name,
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
SELECT
    customer_id,
    category_name,
    season_name,
    total_amount,
    order_id,
    order_size,
    rn
FROM cte_sales;
