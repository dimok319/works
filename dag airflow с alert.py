from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import time as ti
import requests as re

# === Telegram ===
TELEGRAM_TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"

def send_telegram(msg):
    re.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def run_pagination():
    try:
        url = "https://jsonplaceholder.typicode.com/posts"

        items = []
        page = 1
        limit = 50

        while True:
            resp = re.get(url, params={"_page": page, "_limit": limit})
            resp.raise_for_status()
            data = resp.json()

            if not data:
                break

            print(f"Проход {page}")
            items.extend(data)

            page += 1
            ti.sleep(2)

        df = pd.DataFrame(items)
        print(df)

    except Exception as e:
        send_telegram(f"❌ DAG pagination_dag упал\n{e}")
        raise

with DAG(
    dag_id="pagination_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    PythonOperator(
        task_id="pagination_task",
        python_callable=run_pagination
    )
