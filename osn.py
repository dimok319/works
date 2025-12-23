import sqlite3
from dataclasses import replace

import pandas as pd
import numpy as np
import warnings
import random

from colorlog import exception

warnings.filterwarnings("ignore")


try:
    conn = sqlite3.connect(r"E:\ТРенировка.db")
    df = pd.read_sql("select * from all_sale", conn)
    df2 =  pd.read_sql("select * from all_sale1", conn)
    df3 = pd.read_sql("select * from dop_data", conn)
    conn.close()
    print("Данные загруженны")

except Exception as e:
    print(f"""Ошибка загрузки данных
{e}""")

df = pd.concat([df, df2])


df = pd.merge(df, df , on = "магазин", how = "left")

pt = df.pivot_table(index = "выручка_руб_x", values = "дней_работы_x",  aggfunc="sum")

gp = df.groupby("магазин")[["возвраты_шт_x", "возвраты_шт_x"]].sum()

df["посетители_x"] = np.where(df["магазин"] == "Магазин_01", df["посетители_x"] * 100, df["посетители_x"])

# df["магазин"] = df["магазин"].str.replace("М", "П")
#
# df = df.drop(1)

df.loc[df["магазин"] == "Пагазин_03", "себестоимость_руб_x"] *= 100000

# ИЗМЕНЕННАЯ ЧАСТЬ С ДАТАМИ
dates = ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05',
         '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10', "2024-01-10"]
# Создаем случайные даты, но одинаковые для одинаковых магазинов
df['дата'] = df['магазин'].apply(lambda x: random.choice(dates))

df = df[["магазин", "дата","продажи_шт_x","выручка_руб_x","посетители_x","возвраты_шт_x","себестоимость_руб_x","площадь_м2_x","сотрудники_x","рейтинг_x","дней_работы_x",
         "продажи_шт_y","выручка_руб_y","посетители_y","возвраты_шт_y","себестоимость_руб_y","площадь_м2_y","сотрудники_y","рейтинг_y", "дней_работы_y"]]

try:
    conn = sqlite3.connect(r"E:\ТРенировка.db")
    df.to_sql("good", conn, if_exists = "replace", index = False)
    conn.close()
except Exception as e:
    print(f"""Ошибка выгрузки 
    {e}""")

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.expand_frame_repr", None)
print(df)

