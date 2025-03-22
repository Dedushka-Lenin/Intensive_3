from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from ControlModel import ControlModel

##########################################################################################

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        s = QPixmap('app/graphics/empty_chart.png')
        s = s.scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio)


        self.schedule = QLabel()                                            # График
        self.schedule.setPixmap(s)


##########################################################################################

        self.now = QSpinBox()                                               # Количество недель
        self.now.setRange(1,10)

        self.button_launch = QPushButton("ЗАПУСК", self)                    #Кнопка ЗАПУСК
        self.button_launch.clicked.connect(self.button_launch_clicked)

##########################################################################################

        column_1 = QVBoxLayout()
        column_1.addWidget(QLabel("", self))
        column_1.addWidget(self.schedule, 0)
        column_1.addStretch()

        column_2 = QVBoxLayout()
        column_2.addWidget(QLabel("", self))
        column_2.addWidget(self.now)
        column_2.addWidget(self.button_launch, 0)
        column_2.addStretch()

        line_main = QHBoxLayout()
        line_main.addLayout(column_1)
        line_main.addLayout(column_2)

        Table = QWidget()
        Table.setLayout(line_main)
        self.Table = Table

##########################################################################################

    def button_launch_clicked(self):
        cm = ControlModel
        cm.predictions(cm, self.now.value()+1)

        s = QPixmap('app\graphics\graphic_week.png')
        s = s.scaled(1000, 1000, Qt.AspectRatioMode.KeepAspectRatio)

        self.schedule.setPixmap(s)