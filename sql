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
    cte.customer_id,
    cte.category_name,
    cte.season_name,
    COALESCE(SUM(cte.total_amount), 0) AS total_sales,
    COUNT(cte.order_id) AS order_count,
    MAX(cte.order_date) AS last_order_date,
    AVG(cte.total_amount) AS average_order_value,
    CASE
        WHEN COUNT(cte.order_id) > 10 THEN 'Frequent'
        ELSE 'Infrequent'
    END AS customer_activity
FROM cte_sales cte
LEFT JOIN product_sales ps ON cte.order_id = ps.order_id
INNER JOIN categories cat ON ps.category_id = cat.category_id
WHERE cte.category_name ILIKE 'Fruits%' 
AND cte.sales_channel_id IN (1, 2, 3)  -- Selecting only certain sales channels
GROUP BY cte.customer_id, cte.category_name, cte.season_name
HAVING SUM(cte.total_amount) > 5000
ORDER BY total_sales DESC;
