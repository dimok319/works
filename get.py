import time
import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/posts"

all_posts = []
page = 1
limit = 10

while True:
    data = requests.get(url, params={"_page": "page", "_limit": "limit"}).json()
    if not data:
        break

    all_posts += data
    page += 1
    print("партия прошла")
    time.sleep(60)

df = pd.DataFrame(all_posts)
print("Всего в списке:", len(df))
print(df.head())
