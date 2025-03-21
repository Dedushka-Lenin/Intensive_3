import sys

from MainMenu import MainMenu

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow

##########################################################################################

class MainWindow(QMainWindow, MainMenu):
    def __init__(self):
        super(MainWindow, self).__init__()  
        self.show()                                     #Создание окна
        self.setWindowTitle("Prediction")
        self.setCentralWidget(self.Table)

##########################################################################################

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setFixedSize(QSize(1200, 580))
    window.setStyleSheet("background-color: #ffffff;")
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()