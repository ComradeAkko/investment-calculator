# inveStratGUI.py by Comrade Akko

import sys
from PyQt5.QtWidgets import (QApplication, QGridLayout, QPushButton, QWidget, 
        QVBoxLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox,
        QDialog, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# based on Python Tutorials @ https://build-system.fman.io/pyqt5-tutorial
class App(QDialog):
    def __init__(self, parent = None):
        super(App, self).__init__(parent)

        self.title = 'Stock/ETF Historical Investment Strategy Calculator'
        
        mainLayout = QGridLayout() 

        # setting where it appears
        self.left = 200
        self.top = 150
        self.width = 1024
        self.height = 527

        # create group boxes
        self.createTickerBoxes()
        self.createStratBoxes()
        self.createStaticNumbersBoxes()
        self.createActiveNumbersBoxes()
        self.createCalculateBox()

        # create and organize the layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.tickerBoxes, 0, 0)
        mainLayout.addLayout(self.stratBoxes, 1, 0)
        mainLayout.addLayout(self.staticNumbersBoxes, 2, 0)
        mainLayout.addLayout(self.activeNumbersBoxes, 3, 0)
        mainLayout.addLayout(self.calculateBox, 4, 0)
        self.setLayout(mainLayout)


        # initializing the app
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.show()
    
    # creates a ticker box
    def createTickerBoxes(self):
        self.tickerBoxes = QHBoxLayout()

        # create ticker line edit
        tickerLineEdit = QLineEdit('')

        tickerLabel = QLabel("&Ticker:")
        tickerLabel.setBuddy(tickerLineEdit)

        # create startdate line edit
        startDLineEdit = QLineEdit('')

        startDLabel = QLabel("&Starting Date (MM/DD/YYYY):")
        startDLabel.setBuddy(startDLineEdit)

        # create enddate line edit
        endDLineEdit = QLineEdit('')

        endDLabel = QLabel("&Ending Date (MM/DD/YYYY):")
        endDLabel.setBuddy(endDLineEdit)

        # adding all widgets to the boxlayout
        self.tickerBoxes.addWidget(tickerLabel)
        self.tickerBoxes.addWidget(tickerLineEdit)
        self.tickerBoxes.addStretch(1)
        self.tickerBoxes.addWidget(startDLabel)
        self.tickerBoxes.addWidget(startDLineEdit)
        self.tickerBoxes.addWidget(endDLabel)
        self.tickerBoxes.addWidget(endDLineEdit)

    # creates a strategy box
    def createStratBoxes(self):
        self.stratBoxes = QHBoxLayout()
        
        # create list of strategies
        stratList = ["BH", "MT", "GX", "DCA", "DMT", "PMT", "GDM", "GPM"]

        # create a strat1 combo box
        strat1ComboBox = QComboBox()
        strat1ComboBox.addItems(stratList)

        strat1Label = QLabel("&Strategy 1:")
        strat1Label.setBuddy(strat1ComboBox)

        # create a strat2 combo box
        strat2ComboBox = QComboBox()
        strat2ComboBox.addItems(stratList)

        strat2Label = QLabel("&Strategy 2:")
        strat2Label.setBuddy(strat2ComboBox)

        # create a strat3 combo box
        strat3ComboBox = QComboBox()
        strat3ComboBox.addItems(stratList)

        strat3Label = QLabel("&Strategy 3:")
        strat3Label.setBuddy(strat3ComboBox)

        # adding all widgets to the boxlayout
        self.stratBoxes.addWidget(strat1Label)
        self.stratBoxes.addWidget(strat1ComboBox)
        self.stratBoxes.addStretch(1)
        self.stratBoxes.addWidget(strat2Label)
        self.stratBoxes.addWidget(strat2ComboBox)
        self.stratBoxes.addStretch(1)
        self.stratBoxes.addWidget(strat3Label)
        self.stratBoxes.addWidget(strat3ComboBox)

    # creates a box that contains the baseSMA and the commission values
    def createStaticNumbersBoxes(self):
        self.staticNumbersBoxes = QHBoxLayout()

        # create a intial capital line edit
        initialLineEdit = QLineEdit('10000')

        initialLabel = QLabel("&Initial capital:")
        initialLabel.setBuddy(initialLineEdit)

        # create baseSMA line edit
        baseSMALineEdit = QLineEdit('200')

        baseSMALabel = QLabel("&Base moving average period (days):")
        baseSMALabel.setBuddy(baseSMALineEdit)

        # create commission line edit
        commissionLineEdit = QLineEdit('5')

        commissionLabel = QLabel("Commission:")
        commissionLabel.setBuddy(commissionLineEdit)

        # adding all widgets to the boxlayout
        self.staticNumbersBoxes.addWidget(initialLabel)
        self.staticNumbersBoxes.addWidget(initialLineEdit)
        self.staticNumbersBoxes.addStretch(1)
        self.staticNumbersBoxes.addWidget(baseSMALabel)
        self.staticNumbersBoxes.addWidget(baseSMALineEdit)
        self.staticNumbersBoxes.addStretch(1)
        self.staticNumbersBoxes.addWidget(commissionLabel)
        self.staticNumbersBoxes.addWidget(commissionLineEdit)

    # creates a box that contains the income, annual income growth rate,
    # and the investment fraction
    def createActiveNumbersBoxes(self):
        self.activeNumbersBoxes = QHBoxLayout()

        # create income line edit
        incomeLineEdit = QLineEdit('0')

        incomeLabel = QLabel("&Annual pre-taxed income:")
        incomeLabel.setBuddy(incomeLineEdit)

        # create annual income growth rate line edit
        aigrLineEdit = QLineEdit('0')

        aigrLabel = QLabel("&Annual income growth rate in decimal (i.e. 0.02):")
        aigrLabel.setBuddy(aigrLineEdit)

        # create annual income growth rate line edit
        invesFracLineEdit = QLineEdit('0')

        invesFracLabel = QLabel("&Fraction of income reserved to investment in decimal (i.e. 0.5):")
        invesFracLabel.setBuddy(invesFracLineEdit)

        # adding all widgets to the boxlayout
        self.activeNumbersBoxes.addWidget(incomeLabel)
        self.activeNumbersBoxes.addWidget(incomeLineEdit)
        self.activeNumbersBoxes.addStretch(1)
        self.activeNumbersBoxes.addWidget(aigrLabel)
        self.activeNumbersBoxes.addWidget(aigrLineEdit)
        self.activeNumbersBoxes.addStretch(1)
        self.activeNumbersBoxes.addWidget(invesFracLabel)
        self.activeNumbersBoxes.addWidget(invesFracLineEdit)
    
    # create a box that contains the calculate button
    def createCalculateBox(self):
        self.calculateBox = QHBoxLayout()

        # create calculate line edit
        calculateButton = QPushButton('Calculate', self)
        calculateButton.setToolTip('This is an example button')
        calculateButton.clicked.connect(self.on_click)

        self.calculateBox.addWidget(calculateButton)



    @pyqtSlot()
    def on_click(self):
        print('Clicked')

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
