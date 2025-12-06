import requests
import pandas as pd
from pandas import json_normalize
import json

def get_and_display_data(url):
    """Получение и отображение данных в виде таблицы"""
    
    try:
        # 1. GET-запрос к API
        print(f"Делаем GET-запрос к: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка на ошибки
        
        # 2. Получаем JSON
        json_data = response.json()
        print(f"Получено JSON данных: {len(json_data) if isinstance(json_data, list) else 1} записей")
        print("-" * 80)
        
        # 3. Преобразуем JSON в DataFrame
        if isinstance(json_data, list):
            df = pd.DataFrame(json_data)
        else:
            df = pd.DataFrame([json_data])
        
        # 4. Выводим информацию о таблице
        print(f"Размер таблицы: {df.shape[0]} строк × {df.shape[1]} столбцов")
        print(f"Столбцы: {', '.join(df.columns.tolist()[:10])}" + 
              ("..." if len(df.columns) > 10 else ""))
        print("-" * 80)
        
        # 5. Выводим таблицу разными способами
        
        # Способ 1: Простой вывод
        print("СПОСОБ 1: Простое представление DataFrame")
        print(df)
        print("\n" + "="*80 + "\n")
        
        # Способ 2: С форматированием
        print("СПОСОБ 2: Форматированная таблица (первые 5 строк)")
        with pd.option_context('display.max_rows', 5, 
                               'display.max_columns', None,
                               'display.width', None,
                               'display.max_colwidth', 20):
            print(df.head())
        
        print("\n" + "="*80 + "\n")
        
        # Способ 3: Только определенные столбцы
        print("СПОСОБ 3: Выбранные столбцы")
        if len(df.columns) > 3:
            selected_cols = df.columns[:3].tolist()
            print(df[selected_cols].head(10))
        
        print("\n" + "="*80 + "\n")
        
        # 6. Дополнительная информация
        print("СПОСОБ 4: Статистика по числовым данным")
        print(df.describe() if not df.select_dtypes(include=['number']).empty 
              else "Нет числовых данных для статистики")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

# Примеры использования с разными API

# Пример 1: Тестовый API с пользователями
print("ПРИМЕР 1: Данные о пользователях")
print("="*80)
url1 = "https://jsonplaceholder.typicode.com/users"
df1 = get_and_display_data(url1)

# Пример 2: API с постами (ограничиваем количество)
print("\n\nПРИМЕР 2: Посты (первые 10)")
print("="*80)
url2 = "https://jsonplaceholder.typicode.com/posts"
# Можем добавить параметры
params = {"_limit": 10}
response = requests.get(url2, params=params)
data = response.json()
df2 = pd.DataFrame(data)
print(df2[['id', 'title', 'userId']].head())

# Пример 3: Публичное API с финансовыми данными
print("\n\nПРИМЕР 3: Финансовые данные (если API доступно)")
print("="*80)
try:
    # Альтернативный API, если первый недоступен
    url3 = "https://api.publicapis.org/entries"
    response = requests.get(url3)
    data = response.json()
    if 'entries' in data:
        df3 = pd.DataFrame(data['entries']).head(5)
        print(df3[['API', 'Description', 'Category']])
except:
    print("API временно недоступно")