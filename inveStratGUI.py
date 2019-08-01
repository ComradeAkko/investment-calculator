# inveStratGUI.py by Comrade Akko

import sys
from PyQt5.QtWidgets import (QApplication, QGridLayout, QPushButton, QWidget, 
        QVBoxLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox,
        QDialog, QLabel, QTableWidget, QTabWidget, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# based on Python Tutorials @ https://build-system.fman.io/pyqt5-tutorial
class App(QDialog):
    def __init__(self, parent = None):
        super(App, self).__init__(parent)

        self.title = 'Stock/ETF Historical Investment Strategy Calculator'
        
        mainLayout = QGridLayout() 

        # create group boxes
        self.createTickerBoxes()
        self.createInstructionBox()
        self.createStratBoxes()
        self.createInitialBox()
        self.createStaticNumbersBoxes()
        self.createIncomeBox()
        self.createAIGRBox()
        self.createInvesFracBox()
        self.createCalculateBox()
        self.createResultsBox()

        # create and organize the layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(self.tickerBoxes, 0, 0)
        mainLayout.addLayout(self.instructBoxes, 1, 0)
        mainLayout.addLayout(self.stratBoxes, 2, 0)
        mainLayout.addLayout(self.initialBox, 3, 0)
        mainLayout.addLayout(self.staticNumbersBoxes, 4, 0)
        mainLayout.addLayout(self.incomeBox, 5, 0)
        mainLayout.addLayout(self.aigrBox, 6, 0)
        mainLayout.addLayout(self.investFracBox, 7, 0)
        mainLayout.addLayout(self.calculateBox, 8, 0)
        mainLayout.addLayout(self.resultsBox, 0, 1, 9, 10)

        mainLayout.setColumnStretch(0,1)
        mainLayout.setColumnStretch(1,10)

        self.createTabs(mainLayout)

        centralLayout = QGridLayout()
        centralLayout.addWidget(self.tabWidget, 0, 0)

        self.setLayout(centralLayout)

        # initializing the app
        self.initUI()
    
    # initializes the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.show()

    # creates the tabs
    def createTabs(self, layout):
        self.tabBoxes = QHBoxLayout()

        self.tabWidget = QTabWidget()

        tab1 = QWidget()
        tab1.setLayout(layout)

        tab2 = QWidget()
        inveStratTextEdit = QTextEdit()
        inveStratTextEdit.setPlainText("Investment strategies\n"
                                    "by ComradeAkko\n\n"
                                    "The following are the investment strategies that can be used with the\n" 
                                    "function. Static strategies are ones where the only capital used is\n" 
                                    "the initial capital. Active strategies include monthly payments.\n\n\n"
                                    "Static Strategies\n\n"
                                    "Buy and Hold (BH):\n"
                                    "After an initial investment, the shares are held for the entirety of\n" 
                                    "its period.\n\n"
                                    "Regular Momentum Trading (MT):\n"
                                    "After an intial investment, the shares are held as long as the price\n" 
                                    "is above its 200-day moving average. If the price is below its 200-day\n"
                                    "moving average, it is sold and transferred to bonds.\n\n"
                                    "Golden-Cross Momentum Trading (GX):\n"
                                    "After an initial investment, shares are held when the price is above\n"
                                    "both its 200-day and 50-day moving average. If the 50-day moving average\n"
                                    "crosses below the 200-day moving average, the shares are sold and\n"
                                    "transferred to bonds.\n\n\n"
                                    "Active Strategies\n\n"
                                    "Dollar-cost Averaging (DCA):\n"
                                    "After the initial lump-sum investment, every month on the 10th,\n"
                                    "as many shares as many are allowed are bought regardless of whether\n"
                                    "prices are high or low. Shares are never sold.\n\n"
                                    "Parallel Momentum Trading (PMT):\n"
                                    "After the intial lump-sum investment,every month on the 10th,\n"
                                    "shares are bought as long as the current price is higher than the 200-day\n"
                                    "moving average. If the current price drops below the 200-day moving\n"
                                    "average, the shares are sold and transferred to bonds. Subsequent\n"
                                    "investment income will be directed to bonds (**parallel** with current\n"
                                    "investments) until the price of the shares rises above the 200-day\n"
                                    "moving average again.\n\n"
                                    "Divergent Momentum Trading (DMT):\n"
                                    "After the initial lump-sum investment, every month on the 10th,\n"
                                    "shares are bought as long as the current price is higher than the 200-day\n"
                                    "moving average. If the current price drops below the 200-day moving\n"
                                    "average, the shares are sold and transferred to bonds. Subsequent\n"
                                    "investment income will be directed to stocks (**divergent** with\n"
                                    "current investmenets) until the price of the shares rises above the\n"
                                    "200-day moving average again.\n\n"
                                    "Golden-Cross Parallel Momentum Trading (GPM):\n"
                                    "A combination of PMT and using both 200-day and 50-day moving averages.\n\n"
                                    "Golden-Cross Divergent Momentum Trading (GDM):\n"
                                    "A combination of DMT and using both 200-day and 50-day moving averages.")
                            
        tab3hbox = QHBoxLayout()
        tab3hbox.setContentsMargins(5, 5, 5, 5)
        tab3hbox.addWidget(inveStratTextEdit)
        tab2.setLayout(tab3hbox)

        self.tabWidget.addTab(tab1, "&Main")
        self.tabWidget.addTab(tab2, "&Investment Strategies")
    
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

    # creates an instruction box
    def createInstructionBox(self):
        self.instructBoxes = QHBoxLayout()

        instructLabel = QLabel("^Note: Dates also accept the answer 'MAX' to indicate the earliest/latest date in both start/end dates.\n")
        
        self.instructBoxes.addWidget(instructLabel)

        

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

    # creates a box that contains the initial capital
    def createInitialBox(self):
        self.initialBox = QHBoxLayout()

        # create a intial capital line edit
        initialLineEdit = QLineEdit('10000')

        initialLabel = QLabel("&Initial capital:")
        initialLabel.setBuddy(initialLineEdit)

        # add the widget
        self.initialBox.addWidget(initialLabel)
        self.initialBox.addWidget(initialLineEdit)

    # creates a box that contains the baseSMA and the commission values
    def createStaticNumbersBoxes(self):
        self.staticNumbersBoxes = QHBoxLayout()

        # create baseSMA line edit
        baseSMALineEdit = QLineEdit('200')

        baseSMALabel = QLabel("&Base moving average period (days):")
        baseSMALabel.setBuddy(baseSMALineEdit)

        # create commission line edit
        commissionLineEdit = QLineEdit('5')

        commissionLabel = QLabel("Commission:")
        commissionLabel.setBuddy(commissionLineEdit)

        # adding all widgets to the boxlayout
        self.staticNumbersBoxes.addWidget(baseSMALabel)
        self.staticNumbersBoxes.addWidget(baseSMALineEdit)
        self.staticNumbersBoxes.addStretch(1)
        self.staticNumbersBoxes.addWidget(commissionLabel)
        self.staticNumbersBoxes.addWidget(commissionLineEdit)

    # creates a box that contains the income
    def createIncomeBox(self):
        self.incomeBox = QHBoxLayout()

        # create income line edit
        incomeLineEdit = QLineEdit('0')

        incomeLabel = QLabel("&Annual pre-taxed income:")
        incomeLabel.setBuddy(incomeLineEdit)

        # adding all widgets to the boxlayout
        self.incomeBox.addWidget(incomeLabel)
        self.incomeBox.addWidget(incomeLineEdit)

    # creates a box containing the aigr
    def createAIGRBox(self):
        self.aigrBox = QHBoxLayout()

        # create annual income growth rate line edit
        aigrLineEdit = QLineEdit('0')

        aigrLabel = QLabel("&Annual income growth rate in decimal (i.e. 0.02):")
        aigrLabel.setBuddy(aigrLineEdit)

        # add the widget
        self.aigrBox.addWidget(aigrLabel)
        self.aigrBox.addWidget(aigrLineEdit)

    # creates a box containing the investment fraction box
    def createInvesFracBox(self):
        self.investFracBox = QHBoxLayout()

        # create the investment fraction line edit
        invesFracLineEdit = QLineEdit('0')

        invesFracLabel = QLabel("&Fraction of income reserved to investment in decimal (i.e. 0.5):")
        invesFracLabel.setBuddy(invesFracLineEdit)

        # add the widget
        self.investFracBox.addWidget(invesFracLabel)
        self.investFracBox.addWidget(invesFracLineEdit)        

    
    # create a box that contains the calculate button
    def createCalculateBox(self):
        self.calculateBox = QHBoxLayout()

        # create calculate line edit
        calculateButton = QPushButton('Calculate', self)
        calculateButton.setToolTip('This is an example button')
        calculateButton.clicked.connect(self.on_click)

        self.calculateBox.addWidget(calculateButton)

    # create a box that contains the results
    def createResultsBox(self):
        self.resultsBox = QHBoxLayout()

        # create a table for results
        resultsTable = QTableWidget(14,5)
        resultsTable.horizontalHeader().setStretchLastSection(True)

        self.resultsBox.addWidget(resultsTable)



    @pyqtSlot()
    def on_click(self):
        print('Clicked')

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
