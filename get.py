import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/posts"
all_posts = []

# Просто делаем 10 запросов - по одному на каждую страницу
for page_num in range(1, 11):
    response = requests.get(url, params={'_page': page_num, '_limit': 10})
    page_data = response.json()
    all_posts.extend(page_data)

# Теперь в all_posts ВСЕ 100 записей
df = pd.DataFrame(all_posts)
print(f"Всего записей: {len(df)}")
print(df.head())