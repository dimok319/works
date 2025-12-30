import pandas as pd
import time as ti
import requests as re

url = "https://jsonplaceholder.typicode.com/posts"

items = []
page = 1
limit = 50  # нормальный размер страницы

while True:
    resp = re.get(url, params={"_page": page, "_limit": limit})
    resp.raise_for_status()
    data = resp.json()


    if not data:
        break
    print(f"Проход {page-1}")


    page += 1
    ti.sleep(2)
    items.extend(data)

df = pd.DataFrame(items)
pd.set_option("display.max_row", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.expand_frame_repr", None)
print(df)

