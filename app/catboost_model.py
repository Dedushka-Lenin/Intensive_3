import pandas as pd
import matplotlib.pyplot as plt

from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, mean_absolute_error

def catBoost():

    data = pd.read_csv('app/date/full.csv')

###############################################################################################

    lag_days = 91  # Количество лагов
    for lag in range(1, lag_days + 1):
        data[f'lag_{lag}'] = data['pfr'].shift(lag)

###############################################################################################

    data.dt = pd.to_datetime(data.dt) # Приводим дату в тип pandas
    data = data.set_index('dt') # Делаем колонку даты индексом, даем ей периодичность месяц ('MS' - month start)

###############################################################################################

    t = list(data.columns)
    t.remove('pfr')

###############################################################################################

    # Разделение на признаки и целевую переменную
    X = data[t]
    y = data['pfr']

###############################################################################################

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

###############################################################################################

    model = CatBoostRegressor(iterations=5000, learning_rate=0.01, depth=6, verbose=0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

###############################################################################################

    plt.figure(figsize=(12, 6))
    plt.plot(y_test.index, y_test, label='Actual', color='blue')
    plt.plot(y_test.index, y_pred, label='Predicted', color='red')
    plt.legend()
    plt.title('Actual vs Predicted')
    plt.xlabel('Дата')
    plt.ylabel('Цена')

    plt.savefig('app/graphics/goida.png')