#!/usr/bin/env python

#investCalc by ComradeAkko

from priceExtractor import getTreasuryData, getStockData, newStockDirectory, newTreasuryDirectory
from datetime import datetime
import csv, operator, math, os


# Classes:

# stores data for easy returning of data
class Data:
    def __init__(self):
        self.initial = 0
        self.assets = 0
        self.cagr = 0
        self.taxes = 0
        self.comissions = 0
        self.pl = 0
        self.div = 0
        self.iDate = 0

# records the data for each purchase of the stock
class Slot:
    def __init__(self, price, quantity, date)
        self.price = price
        self.quantity = quantity
        self.date = date

# records data for each purchase of a 10 year treasury note
class Nlot:
    def __init__(self, amount, rate, date)
        self.amount = amount
        self.rate = rate
        self.date = date

# returns a boolean based on whether the csv file contains data
def dataExists(datePath, limit = 1):
    # opening the file
    file = open(datePath)
    data = csv.reader(Path)

    # summing up the number of rows
    rowCount = sum(1 for row in data)

    # closing the file
    file.close()
    
    # subtracting the header
    rowCount -= 1

    if rowCount >= limit:
        return True
    else:
        return False


# returns a boolean based on whether the csv file contains a date or not
def timeExists(date, dataPath):
    file = open(dataPath)
    data = csv.reader(file)

    # if there are any data points to search dates
    if dataExists(dataPath):
        # skipping the header
        next(data)

        # for every row of data
        for row in data:
            # if the row contains the date return True
            if row[0] == date:
                file.close()
                return True
        
        # if the for loop did not return True for its entire length,
        # return False
        file.close()
        return False
    
# returns the value of whatever dividend paid or stock fraction split
# assumes the date and value exists
def getDivSplit(date,dataPath):
    file = open(dataPath)
    data = csv.reader(file)

    # cycles through the row till it finds the relevant date
    for row in data:
        if row[0] == date:
            file.close()
            return row[1]

# returns the 10 year treasury note yield for stated month
def getNoteYield(date, datapath)
    file = open(dataPath)
    data = csv.reader(file)
    
    # convert the current date into datetime format
    currDate = datetime.strptime(date, "%Y-%m-%d")

    # cycles through the row till it finds the relevant date
    for row in data:
        # convert csv dates to datetime format
        rowDate = datetime.strptime(row[0], "%Y-%m-%d")

        # if the year and month match, return the treasury yield rate
        if rowDate.month == currDate.month and rowDate.year == currDate.year:
            file.close()
            return row[1]
    


# returns the federal 2019 tax rate based on income
def fedTax(income):
    if income <= 9700:
        return .1
    else if income <= 39745:
        return .12
    else if income <= 84200:
        return .22
    else if income <= 160725:
        return .24
    else if income <= 204100:
        return .32
    else if income <= 510300:
        return .35
    else:
        return .37

# returns the federal 2019 tax rate for dividends
def divTax(bracket):
    if bracket <.25:
        return 0
    else if bracket < .35:
        return .15
    else:
        return .2

# calculates compound annual growth rate
def cagr(bb, eb, initialDate, currentDate):
    # convert csv dates to date time
    initialDate = datetime.strptime(initialDate, "%Y-%m-%d")
    currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

    # get the difference in years
    n = currentDate.year - initialDate.year

    # return cagr
    return (eb^(1/n))/bb - 1

# calculates the current moving average based on the period
# and the current date
def movingAverage(period, date, dataPath):
    file = open(dataPath)
    # get the csv file
    data = csv.reader(file)
    index = 0

    # figure out which index holds the current date
    for count, row in enumerate(data):
        if date == row[0]:
            index = count
            break

    # isolate the relevant rows
    movingAverageRows = [row for idx, row in enumerate(reader) if idx in (index - period,index)]

    # calculate the current sum
    sum = 0
    for row in movingAverageRows:
        sum += row[4]
    
    # get the average
    SMA = sum/period

    file.close()
    
    return SMA


# returns data for the Buy and Hold strat
def BH(ticker, cash, income, commission):
    # initialize the data
    data = Data()

    #set initial cash
    data.initial = cash

    # account for comissions
    cash -= commission
    data.comissions += commission

    #create the file paths
    pricePath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_price.csv"
    divPath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_dividend.csv"
    splitPath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_split.csv"
    
    # get the csv file
    priceF = open(pricePath)
    prices = csv.reader(priceF)

    # skipping the header
    next(prices)

    # skip the first 200 days
    for i in range(200)
        next(prices)

    buyRow = next(prices)
    
    # get the opening price for the 201st day
    price = buyRow[1]
    
    # get the current date and record it in the data
    date = buyRow[0]
    data.iDate = date

    # get the quantity of how many stocks you can buy
    quantity = math.floor(cash/price)

    # subtract the amount that I bought from the cash
    cash -= price * quantity

    # store in the information in a stock lot
    slot = Slot(price, quantity, date)

    # for every price, check to see if there was a stock split or a dividend issued
    for row in prices:
        # if there is any data for splitting stocks
        if dataExists(splits):
            # if any of the dates appear in the stock split data
            if timeExists(row[0],splitPath):
                # get the fraction of splitting
                fraction = getDivSplit(row[0], splitPath)
                slot.quantity = math.floor(slot.quantity / fraction)
        
        # if there is any data for dividends
        if dataExists(dividends):
            # if any of the dates appear in the dividend data
            if timeExists(row[0], divPath):
                # get the dividend for the day and calculate the money gained
                d = getDivSplit(row[0], divPath)
                cash += d * slot.quantity * (1 - divTax(fedTax(income)))

                # record the dividends into data
                data.div += d * slot.quantity * (1 - divTax(fedTax(income)))

                # record the taxes paid
                data.taxes += d * slot.quantity * divTax(fedTax(income))
    
    prices = list(prices)
    # calculate profit/loss
    data.pl = (prices[-1][4] - slot.price) * slot.quantity

    # calculate total assets
    data.assets = cash + (prices[-1][4] * slot.quantity)

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[-1][0])

    # close file
    priceF.close()

    return data



def MT(ticker, baseSMA, income, cash, commission):
    # initialize the data
    data = Data()

    #set initial cash
    data.initial = cash

    #create the file paths
    pricePath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_price.csv"
    divPath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_dividend.csv"
    splitPath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_split.csv"
    notePath = os.getcwd() + "\\notes\\notes.csv"
    
    # get the csv file
    priceF = open(pricePath)
    prices = csv.reader(priceF)

    # skipping the header
    next(prices)

    # skip the first 200 days
    for i in range(199)
        next(prices)
    
    # listify the csv.reader file
    prices = list(prices)

    # calculate the current moving average
    sma = movingAverage(baseSMA, price[0][0], pricePath)

    # if the closing price of the previous day is greater than or equal to the sma
    if prices[0][4] >= sma:
        # buy the stock at the current price
        slot = Slot()
        slot.price = prices[1][1]
        slot.quantity = math.floor(cash/price)
        slot.date = prices[1][0]
        
        # subtract the amount used
        cash -= slot.price * slot.quantity

        # account for comissions
        cash -= commission
        data.comissions += commission

        # mark the boolean for keeping track of whether stocks or bonds have been bought
        boughtStock = True
    
    # if the current opening price is less than the sma
    else:
        # buy treasury notes
        nlot = Nlot()
        nlot.rate = getNoteYield(prices[1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[1][0]

        # account for comissions
        cash -= commission
        data.comissions += commission

        boughtStock = False


    # for every remaining price data
    for i in range(1, len(prices)):
        # calculate the current moving average
        sma = movingAverage(baseSMA, price[i][0], pricePath)

        # if the current price is greater than or equal to the sma
        if prices[i][0] >= sma:





    


def GX(ticker, baseSMA, cash, commission):

def investCalc(ticker, baseSMA = 200, initial, income, investFrac, aigr, strat, monthly, commission = 5):
    stockPath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker
    notesPath = os.getcwd() + "\\notes\\notes.csv"

    # make sure the dataset actually exists
    if os.path.isfile(stockPath + "_split.csv") == False or os.path.isfile(stockPath + "_price.csv") == False or os.path.isfile(stockPath + "_dividend.csv") == False:
        getStockData(ticker)
    if os.path.isfile(notesPath) == False:
        getTreasuryData()
    
    # getting the csv file
    stockPricePath = stockPath + "_price.csv"

    # if the there are enough data points for the SMA being used
    if dataExists(stockPricePath, baseSMA):
        if strat == "MT":
            MTdata = MT(ticker, baseSMA, commission)
            BHdata = BH(ticker, initial, income, commission)
        
        else if strat == "GX":
            GXdata = GX()
            BHdata = BH()
        
        else if strat == "DMT":
        
        else if strat == "PMT":

        else if strat == "GPM":

        else if strat == "GDM":

        else:
            print("strategy does not exist, please input a valid strategy")


    else:
        print("Stock data does not have enough data points for this baseSMA")

    




# calculate buying and selling

# disclaimer about how the current model doesn't use historical data on tax rates
# disclaimer about how the current model doesn't use historical capital gains tax rates 