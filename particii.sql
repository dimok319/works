-- Создаем таблицу заказов с партиционированием по месяцам
CREATE TABLE orders (
    id SERIAL,
    order_date DATE NOT NULL,
    customer_id INT,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (order_date);

-- Создаем партиции по месяцам
CREATE TABLE orders_2024_01 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Вставляем данные
INSERT INTO orders (order_date, customer_id, amount) 
VALUES ('2024-01-15', 1, 1000);  -- Попадет в orders_2024_01

INSERT INTO orders (order_date, customer_id, amount)
VALUES ('2024-02-20', 2, 2000);  -- Попадет в orders_2024_02

-- При запросе PostgreSQL автоматически выберет нужную партицию
SELECT * FROM orders WHERE order_date >= '2024-02-01';
