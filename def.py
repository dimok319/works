import pandas as pd
import numpy as np

def process_users(df):
    # Копируем, чтобы не менять исходный
    df = df.copy()
    
    # 1. Фильтр по возрасту
    df = df[(df['age'] >= 18) & (df['age'] <= 100)]
    
    # 2. Заполнение пропусков в email
    df['email'] = df['email'].fillna('unknown@example.com')
    
    # 3. Категория по баллам
    def categorize(score):
        if score >= 80:
            return 'high'
        elif score >= 50:
            return 'medium'
        else:
            return 'low'
    
    df['score_category'] = df['score'].apply(categorize)
    
    # 4. Преобразование даты
    df['join_date'] = pd.to_datetime(df['join_date'])
    
    # 5. Сброс индекса
    df = df.reset_index(drop=True)
    
    return df
