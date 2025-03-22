import matplotlib.pyplot as plt
import pandas as pd

from catBoost import catBoost


class ControlModel:

    def predictions(self, now):

        data = pd.read_csv('app/date/full.csv')

        data.dt = pd.to_datetime(data.dt) # Приводим дату в тип pandas
        data = data.set_index('dt') # Делаем колонку даты индексом, даем ей периодичность месяц ('MS' - month start)

        lag_days = 400  # Количество лагов
        for lag in range(1, lag_days + 1):
            data[f'lag_{lag}'] = data['pfr'].shift(lag)

        t = list(data.columns)
        t.remove('pfr')


        train = data.head(-11)
        test = data.tail(11)
        test = test.head(now)

        X_train = train[t]
        y_train = train['pfr']

        X_test = test[t]
        y_test = test['pfr']
        
        y_pred = catBoost(X_train, y_train, X_test)

        self.plotting(y_test, y_pred)

###############################################################################################

    def plotting(y_test, y_pred):

        plt.figure(figsize=(12, 6))
        plt.plot(y_test.index, y_test, label='Actual', color='blue')
        plt.plot(y_test.index, y_pred, label='Predicted', color='red')
        plt.legend()
        plt.title('Actual vs Predicted')
        plt.xlabel('Дата')
        plt.ylabel('Цена')

        plt.savefig('app/graphics/graphic_week.png')