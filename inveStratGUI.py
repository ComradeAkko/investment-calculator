# inveStratGUI.py by Comrade Akko

import sys
from PyQt5.QtWidgets import (QApplication, QGridLayout, QPushButton, QWidget, 
        QVBoxLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox,
        QDialog, QLabel, QTableWidget, QTabWidget, QTextEdit, QTableWidgetItem,
        QCheckBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from investCalc import *
from priceExtractor import *
from helperFunc import *

# based on Python Tutorials @ https://build-system.fman.io/pyqt5-tutorial
class App(QDialog):
    def __init__(self, parent = None):
        super(App, self).__init__(parent)

        self.title = 'Stock/ETF Historical Investment Strategy Calculator'

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
        self.createExtraBasicBox()
        self.createExtraDateBox()
        self.createErrorBox()
        self.createFinalIncomeBox()

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
        mainLayout.addLayout(self.errorBox, 9, 0)
        mainLayout.addLayout(self.resultsBox, 0, 1, 7, 10)
        mainLayout.addLayout(self.extraBasicBox, 7, 1)
        mainLayout.addLayout(self.extraDateBox, 8, 1)
        mainLayout.addLayout(self.finalIncomeBox, 9, 1)

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

        self.tabWidget = QTabWidget()

        tab1 = QWidget()
        tab1.setLayout(layout)

        tab2 = QWidget()
        guideLabel = QLabel("Check boxes for data to be updated:")
        stockLineEdit = QLineEdit("")
        stockCheck = QCheckBox("Ticker: ")

        notesCheck = QCheckBox("Treasury Notes")
        
        tickerCheck = QCheckBox("Ticker List")

        refreshButton = QPushButton("Update Data")
        refreshButton.clicked.connect(self.clickRefresh)

        errorMessage = QLabel("")

        tab2Box = QVBoxLayout()
        tab2miniBox = QHBoxLayout()

        tab2miniBox.addWidget(stockCheck)
        tab2miniBox.addWidget(stockLineEdit)

        tab2Box.addWidget(guideLabel)
        tab2Box.addLayout(tab2miniBox)
        tab2Box.addWidget(notesCheck)
        tab2Box.addWidget(tickerCheck)
        tab2Box.addWidget(refreshButton)
        tab2Box.addWidget(errorMessage)


        tab2.setLayout(tab2Box)


        tab3 = QWidget()
        inveStratTextEdit = QTextEdit()
        inveStratTextEdit.setPlainText("Investment strategies\n"
                                    "by ComradeAkko\n\n"
                                    "The following are the investment strategies that can be used with the\n" 
                                    "function. Static strategies are ones where the only capital used is\n" 
                                    "the initial capital. Active strategies include monthly payments.\n\n\n"
                                    "Static Strategies\n\n"
                                    "Buy and Hold (BH):\n"
                                    "After an initial investment, the shares are held for the entirety of\n" 
                                    "its period. Dividends are not reinvested.\n\n"
                                    "Regular Momentum Trading (MT):\n"
                                    "After an intial investment, the shares are held as long as the price\n" 
                                    "is above its 200-day moving average. If the price is below its 200-day\n"
                                    "moving average, it is sold and transferred to bonds. Dividends are reinvested\n"
                                    "when a trade is made.\n\n"
                                    "Golden-Cross Momentum Trading (GX):\n"
                                    "After an initial investment, shares are held when the price is above\n"
                                    "both its 200-day and 50-day moving average. If the 50-day moving average\n"
                                    "crosses below the 200-day moving average, the shares are sold and\n"
                                    "transferred to bonds. Dividends are reinvested\n"
                                    "when a trade is made.\n\n\n"
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
        tab3.setLayout(tab3hbox)

        self.tabWidget.addTab(tab1, "&Main")
        self.tabWidget.addTab(tab2, "&Updating Data")
        self.tabWidget.addTab(tab3, "&Investment Strategies")
    
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
        calculateButton.clicked.connect(self.clickCalculate)

        self.calculateBox.addWidget(calculateButton)

    # create a box that contains the results
    def createResultsBox(self):
        self.resultsBox = QHBoxLayout()

        # create a table for results
        resultsTable = QTableWidget(7,3)
        resultsTable.horizontalHeader().setStretchLastSection(True)

        # Inputting info
        header0 = QTableWidgetItem("Commission:")
        headerz = QTableWidgetItem("Commission:")
        header1 = QTableWidgetItem("Taxes:")
        header2 = QTableWidgetItem("Treasury Yield:")
        header3 = QTableWidgetItem("Dividend received:")
        header4 = QTableWidgetItem("Profit/loss from trading:")
        header5 = QTableWidgetItem("Final Assets:")
        header6 = QTableWidgetItem("CAGR:")
        header7 = QTableWidgetItem("strategy1")
        header8 = QTableWidgetItem("strategy2")
        header9 = QTableWidgetItem("strategy3")
        resultsTable.setVerticalHeaderItem(0, header0)
        resultsTable.setVerticalHeaderItem(1, header1)
        resultsTable.setVerticalHeaderItem(2, header2)
        resultsTable.setVerticalHeaderItem(3, header3)
        resultsTable.setVerticalHeaderItem(4, header4)
        resultsTable.setVerticalHeaderItem(5, header5)
        resultsTable.setVerticalHeaderItem(6, header6)
        resultsTable.setHorizontalHeaderItem(0, header7)
        resultsTable.setHorizontalHeaderItem(1, header8)
        resultsTable.setHorizontalHeaderItem(2, header9)


        self.resultsBox.addWidget(resultsTable)
    
    # create more results boxes that contain the ticker and initial capital info
    def createExtraBasicBox(self):
        self.extraBasicBox = QHBoxLayout()

        # create labels to contain the basic info
        basicTickerLabel = QLabel("Ticker: ")
        basicInitialLabel = QLabel("Initial Capital: ")
        self.extraBasicBox.addWidget(basicTickerLabel)
        self.extraBasicBox.addWidget(basicInitialLabel)

    # create more results boxes that contain the start/end date info
    def createExtraDateBox(self):
        self.extraDateBox = QHBoxLayout()

        # create labels to contain the basic info
        basicStartDate = QLabel("Start Date: ")
        basicEndDate = QLabel("End date: ")
        self.extraDateBox.addWidget(basicStartDate)
        self.extraDateBox.addWidget(basicEndDate)

    # create error boxes that display errors
    def createErrorBox(self):
        self.errorBox = QHBoxLayout()
        errorLabel = QLabel(" ")
        self.errorBox.addWidget(errorLabel)
    
    # creates an error box that displays final incomes
    def createFinalIncomeBox(self):
        self.finalIncomeBox = QHBoxLayout()
        finalIncomeLabel = QLabel("Final Income: ")
        self.finalIncomeBox.addWidget(finalIncomeLabel)

    # what to do when calculate button is pushed
    @pyqtSlot()
    def clickCalculate(self):
        # get all the inputs
        ticker = self.tickerBoxes.itemAt(1).widget().text()
        startDate = self.tickerBoxes.itemAt(4).widget().text()
        endDate = self.tickerBoxes.itemAt(6).widget().text()
        strat1 = self.stratBoxes.itemAt(1).widget().currentText()
        strat2 = self.stratBoxes.itemAt(4).widget().currentText()
        strat3 = self.stratBoxes.itemAt(7).widget().currentText()

        # make sure the values are all numbers
        numbers = True
        try:
            capital = float(self.initialBox.itemAt(1).widget().text())
            sma = int(self.staticNumbersBoxes.itemAt(1).widget().text())
            commission = float(self.staticNumbersBoxes.itemAt(4).widget().text())
            income = float(self.incomeBox.itemAt(1).widget().text())
            aigr = float(self.aigrBox.itemAt(1).widget().text())
            invesFrac = float(self.investFracBox.itemAt(1).widget().text())
        except ValueError:
            numbers = False
        
        if numbers:
            # get the results
            results = investCalc(ticker, startDate, endDate, capital, income, strat1, strat2, strat3, sma, commission, invesFrac, aigr)

            if results.errorBoo == False:
                # sort out the data
                data1 = results.strat1
                data2 = results.strat2
                data3 = results.strat3

                # print the results
                table = self.resultsBox.itemAt(0).widget()

                # for strategy 1
                strat1 = QTableWidgetItem(data1.type)
                assets1 = QTableWidgetItem(str(round(data1.assets,2)))
                cagr1 = QTableWidgetItem(str(round(data1.cagr,4)))
                taxes1 = QTableWidgetItem(str(round(data1.taxes,2)))
                commission1 = QTableWidgetItem(str(round(data1.comissions,2)))
                pl1 = QTableWidgetItem(str(round(data1.pl,2)))
                div1 = QTableWidgetItem(str(round(data1.div,2)))
                treasury1 = QTableWidgetItem(str(round(data1.treasury,2)))

                table.setHorizontalHeaderItem(0, strat1)
                table.setItem(0,0, commission1)
                table.setItem(1,0, taxes1)
                table.setItem(2,0, treasury1)
                table.setItem(3,0, div1)
                table.setItem(4,0, pl1)
                table.setItem(5,0, assets1)
                table.setItem(6,0, cagr1)

                # for strategy 2
                strat2 = QTableWidgetItem(data2.type)
                assets2 = QTableWidgetItem(str(round(data2.assets,2)))
                cagr2 = QTableWidgetItem(str(round(data2.cagr,4)))
                taxes2 = QTableWidgetItem(str(round(data2.taxes,2)))
                commission2 = QTableWidgetItem(str(round(data2.comissions,2)))
                pl2 = QTableWidgetItem(str(round(data2.pl,2)))
                div2 = QTableWidgetItem(str(round(data2.div,2)))
                treasury2 = QTableWidgetItem(str(round(data2.treasury,2)))

                table.setHorizontalHeaderItem(1, strat2)
                table.setItem(0,1, commission2)
                table.setItem(1,1, taxes2)
                table.setItem(2,1, treasury2)
                table.setItem(3,1, div2)
                table.setItem(4,1, pl2)
                table.setItem(5,1, assets2)
                table.setItem(6,1, cagr2)

                # for strategy 3
                strat3 = QTableWidgetItem(data3.type)
                assets3 = QTableWidgetItem(str(round(data3.assets,2)))
                cagr3 = QTableWidgetItem(str(round(data3.cagr,4)))
                taxes3 = QTableWidgetItem(str(round(data3.taxes,2)))
                commission3 = QTableWidgetItem(str(round(data3.comissions,2)))
                pl3 = QTableWidgetItem(str(round(data3.pl,2)))
                div3 = QTableWidgetItem(str(round(data3.div,2)))
                treasury3 = QTableWidgetItem(str(round(data3.treasury,2)))

                table.setHorizontalHeaderItem(2, strat3)
                table.setItem(0,2, commission3)
                table.setItem(1,2, taxes3)
                table.setItem(2,2, treasury3)
                table.setItem(3,2, div3)
                table.setItem(4,2, pl3)
                table.setItem(5,2, assets3)
                table.setItem(6,2, cagr3)

                # set the other basic info
                tickerBasics = "Ticker: " + results.ticker
                initialBasics = "Initial Capital: " + str(round(capital,2))

                startBasics = "Start Date: " + data1.iDate
                endBasics = "End Date: " + data1.pDate

                incomeBasics = "Final Income: " + str(round(results.income,2))

                self.extraBasicBox.itemAt(0).widget().setText(tickerBasics)
                self.extraBasicBox.itemAt(1).widget().setText(initialBasics)
                self.extraDateBox.itemAt(0).widget().setText(startBasics)
                self.extraDateBox.itemAt(1).widget().setText(endBasics)
                self.finalIncomeBox.itemAt(0).widget().setText(incomeBasics)

                error = " "
                self.errorBox.itemAt(0).widget().setText(error)

            else:
                error = "Error: " + results.errorMess
                self.errorBox.itemAt(0).widget().setText(error)

        else:
            error = "Error: One or more of the number inputs do not contain valid numbers, please try again."
            self.errorBox.itemAt(0).widget().setText(error)
    
    # what to do when the refresh button is pushed
    def clickRefresh(self):
        ticker = self.tabWidget.widget(1).layout().itemAt(1).layout().itemAt(1).widget().text()
        stockBool = self.tabWidget.widget(1).layout().itemAt(1).layout().itemAt(0).widget().isChecked()
        notesBool = self.tabWidget.widget(1).layout().itemAt(2).widget().isChecked()
        tickerBool = self.tabWidget.widget(1).layout().itemAt(3).widget().isChecked()

        # if the stock check box is checked
        if stockBool:
            # if the ticker exists
            if tickerExists(ticker):
                getStockData(ticker)
                if notesBool:
                    getTreasuryData()
                if tickerBool:
                    getTickerList()
                self.tabWidget.widget(1).layout().itemAt(5).widget().setText("Update done.")
            else:
                self.tabWidget.widget(1).layout().itemAt(5).widget().setText("Error: ticker does not exist")
        else:
            if notesBool:
                getTreasuryData()
            if tickerBool:
                getTickerList()
            self.tabWidget.widget(1).layout().itemAt(5).widget().setText("Update done.")
            
        

  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
