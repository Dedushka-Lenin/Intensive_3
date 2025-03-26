import pandas as pd

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from ControlModel import ControlModel

##########################################################################################

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        s = QImage('app/graphics/empty_chart.png')


        self.schedule = QLabel()                                            # График
        self.schedule.setPixmap(QPixmap.fromImage(s))


##########################################################################################

        self.cd = QDateEdit()                                               # Дата
        self.cd.setDate(QDate(2023, 1, 2))
        self.cd.setDisplayFormat("d.MM.yyyy")

        self.now = QSpinBox()                                               # Количество недель
        self.now.setRange(1,10)

        self.button_launch = QPushButton("ЗАПУСК", self)                    #Кнопка ЗАПУСК
        self.button_launch.clicked.connect(self.button_launch_clicked)

        self.button_launch.setStyleSheet("""
            QPushButton {
                border: 2px solid #000000;    /* Цвет обводки */
                border-radius: 5px;           /* Закругление углов */
                background-color: white;      /* Цвет фона */
                color: #000000;               /* Цвет текста */
            }
            QPushButton:hover {
                background-color: #808080;    /* Цвет фона при наведении */
                color: white;                 /* Цвет текста при наведении */
            }
            QPushButton:pressed {
                background-color: #000000;    /* Цвет фона при нажатии */
            }
        """)

        self.sign = QLabel(self)
        self.sign.setWordWrap(True)
        self.sign.setMaximumWidth(180)

##########################################################################################

        column_1 = QVBoxLayout()
        column_1.addWidget(self.schedule, 0)
        column_1.addStretch()

        column_2 = QVBoxLayout()
        column_2.addStretch()
        column_2.addWidget(self.cd)
        column_2.addWidget(self.now)
        column_2.addWidget(self.button_launch, 0)
        column_2.addStretch()
        column_2.addWidget(self.sign, 0)

        line_main = QHBoxLayout()
        line_main.addLayout(column_1)
        line_main.addLayout(column_2)

        Table = QWidget()
        Table.setLayout(line_main)
        self.Table = Table

##########################################################################################

    def button_launch_clicked(self):

        date = self.cd.text().split('.')
        date = pd.to_datetime(f'{date[2]}.{date[1]}.{date[0]}')

        if pd.to_datetime('2023-01-02 00:00:00') < date:
            self.sign.setText('Установленная вами дата больше верхнего порога \n верхний порог - 2.01.2023')

        elif pd.to_datetime('2022-10-03 00:00:00') > date:
            self.sign.setText('Установленная вами дата меньше нижнего порога \n нижний порог - 3.10.2022')

        else:
            self.sign.setText('')

            cm = ControlModel
            pred, dt = cm.predictions(cm, self.now.value()+1, date)

            s = QPixmap('app\graphics\graphic_week.png')
            s = s.scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio)

            self.schedule.setPixmap(s)

            advice = 'Рекомедованные даты для закупок:'

            for i in range(len(pred)):

                c = 0

                for j in range(i+1,len(pred)):

                    if pred[i] > pred[j]:
                        c = j - i
                        break
                        
                    c = len(pred) - i

                if c != 0:
                    t = str(dt[i]).split(' ')[0]
                    t = t.split('-')

                    advice += f'\n    {t[2]}.{t[1]}.{t[0]}({i}) - на {c} {self.declination(c)}'

            self.sign.setText(advice)

    def declination(self, week):
        if week == 1:
            return 'неделю'
        elif week in [2, 3, 4]:
            return 'недели'
        else:
            return 'недель'