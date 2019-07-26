# inveStratGUI.py by Comrade Akko

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# based on Python Tutorials @ https://pythonspot.com/pyqt5-window/
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Stock/ETF Historical Investment Strategy Calculator'
        self.left = 200
        self.top = 150
        self.width = 1024
        self.height = 527
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        calculate = QPushButton('Calculate', self)
        calculate.setToolTip('This is an example button')
        calculate.move(50,450)
        calculate.clicked.connect(self.on_click)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('Clicked')

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
