import pandas as pd
import psycopg2

# Подключение
conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="postgres",
    password="12345",
    port="5432"
)

# Читаем данные
df = pd.read_sql("SELECT * FROM users", conn)
conn.close()

print(df.head())  # первые 5 строк
print(f"\nВсего записей: {len(df)}")