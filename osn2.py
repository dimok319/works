import sqlite3
from dataclasses import replace

import pandas as pd
import numpy as np
import warnings

from colorlog import exception

warnings.filterwarnings("ignore")


try:
    conn = sqlite3.connect(r"E:\ТРенировка.db")
    df = pd.read_sql("select * from all_sale", conn)
    df2 =  pd.read_sql("select * from all_sale1", conn)
    df3 = pd.read_sql("select * from dop_data2", conn)
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

df["магазин"] = df["магазин"].str.replace("М", "П")

df = df.drop(1)

df.loc[df["магазин"] == "Пагазин_03", "себестоимость_руб_x"] *= 100000

dates = ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
df['дата'] = [dates[i % len(dates)] for i in range(len(df))]

df = df[["магазин", "дата","продажи_шт_x","выручка_руб_x","посетители_x","возвраты_шт_x","себестоимость_руб_x","площадь_м2_x","сотрудники_x","рейтинг_x","дней_работы_x",
         "продажи_шт_y","выручка_руб_y","посетители_y","возвраты_шт_y","себестоимость_руб_y","площадь_м2_y","сотрудники_y","рейтинг_y", "дней_работы_y"]]

# try:
#     conn = sqlite3.connect(r"E:\ТРенировка.db")
#     df.to_sql("good", conn, if_exists = "replace", index = False)
#     conn.close()
# except Exception as e:
#     print(f"""Ошибка выгрузки
#     {e}""")

df2 = df[["магазин", "площадь_м2_x", "продажи_шт_x"]]

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.expand_frame_repr", None)

import matplotlib.pyplot as plt

df2 = df2.sort_values(by = "площадь_м2_x")
y = df2["площадь_м2_x"]
x = df2["магазин"]

plt.plot(x, y)
plt.show()

plt.pie(df2["площадь_м2_x"], labels=df2["магазин"], autopct="%.1f%%")
plt.show()



print(df)
print(df2)

