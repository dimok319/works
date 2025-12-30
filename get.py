import pandas as pd
import time as ti
import requests as re

url = "https://jsonplaceholder.typicode.com/posts"

items = []
page = 1
limit = 20  # нормальный размер страницы

while True:
    resp = re.get(url, params={"_page": page, "_limit": limit})
    resp.raise_for_status()
    data = resp.json()

    if not data:
        break
    print(f"Проход {page-1}")
    items.extend(data)

    page += 1
    ti.sleep(1)

df = pd.DataFrame(items)
