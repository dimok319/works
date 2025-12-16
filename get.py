import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/users"
df = pd.DataFrame(requests.get(url).json())
print(df.head())
