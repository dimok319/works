#пагинации
import pandas as pd
import time as ti
import requests as re
import json

url = "https://jsonplaceholder.typicode.com/posts"

all = []
page = 1
limit = 100
num = 0

while True:
    data = re.get(url, params= {"_page": "page", "_limit":"Limit"}).json()
    if not data:
        break
    page += 1
    num += 1
    print(f"{num} проход")
    ti.sleep(10)

df = pd.DataFrame(all)
print(df)
