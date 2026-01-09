-- Создаем таблицу пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP
);

-- Создаем индекс по email для быстрого поиска
CREATE INDEX idx_users_email ON users(email);

-- Проверяем работу индекса
EXPLAIN SELECT * FROM users WHERE email = 'ivan@example.com';
