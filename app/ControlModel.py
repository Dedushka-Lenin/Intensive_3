import matplotlib.pyplot as plt
import pandas as pd

from catBoost import catBoost

from statsmodels.tsa.seasonal import seasonal_decompose


class ControlModel:

    def predictions(self, now, date):

        data = pd.read_csv('app/date/full.csv')

        data.dt = pd.to_datetime(data.dt) # Приводим дату в тип pandas
        data = data.set_index('dt') # Делаем колонку даты индексом, даем ей периодичность месяц ('MS' - month start)

        decomposition = seasonal_decompose(data['pfr'], model='additive')

        data['trend'] = decomposition.trend
        data['seasonal'] = decomposition.seasonal
        data['residual'] = decomposition.resid


        lag_days = 50  # Количество лагов
        for lag in range(1, lag_days + 1):
            data[f'lag_{lag}'] = data['pfr'].shift(lag)

        t = list(data.columns)
        t.remove('pfr')

        test_start = date
        test_stop = date + pd.Timedelta(days=now*7)

        test = data[(data.index >= test_start) & (data.index < test_stop)]

        X_test = test[t]
        y_test = test['pfr']
        
        y_pred = catBoost(X_test)

        self.plotting(y_test, y_pred, now)

        return y_pred, test.index

###############################################################################################

    def plotting(y_test, y_pred, now):

        plt.figure(figsize=(12, 6), dpi=200)
        plt.plot(y_test.index, y_pred, label='Predicted', color='red')
        plt.plot(y_test.index, y_test, label='Actual', color='blue')
        plt.xticks(y_test.index, rotation=45)
        plt.legend(fontsize=12)
        plt.title('Actual vs Predicted')
        plt.xlabel('Дата')
        plt.ylabel('Цена')

        for i, (date, price) in enumerate(zip(y_test.index[1:], y_pred[1:]), start=1):

            text_y = price + 2**now  # Поднимаем текст на 5 единиц

            # Проверяем, не выходит ли текст за пределы графика
            if text_y > plt.ylim()[1] - 2**(now-1):  # Если текст выходит за верхнюю границу
                text_y = price - 2**now  # Смещаем текст вниз
            
            plt.annotate(f'Неделя №{i}',
                         xy=(date, price),  # Координаты точки
                         xytext=(date, text_y),  # Положение текста
                         arrowprops=dict(arrowstyle='-', color='black'),  # Стиль стрелки
                         fontsize=9, 
                         ha='center', 
                         va='bottom', 
                         color='black')  # Цвет текста
            
        plt.tight_layout()

        plt.savefig('app/graphics/graphic_week.png')