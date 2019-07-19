#!/usr/bin/env python

#investCalc by ComradeAkko

from priceExtractor import getTreasuryData, getStockData, newStockDirectory, newTreasuryDirectory
from datetime import datetime
import csv, operator, math, os


# Classes:

# stores data for easy returning of data
class Data:
    def __init__(self):
        self.type = 0
        self.initial = 0
        self.assets = 0
        self.cagr = 0
        self.taxes = 0
        self.comissions = 0
        self.pl = 0
        self.div = 0
        self.iDate = 0
        self.pDate = 0

# records the data for each purchase of the stock
class Slot:
    def __init__(self):
        self.price = 0
        self.quantity = 0
        self.date = 0

# records data for each purchase of a 10 year treasury note
class Nlot:
    def __init__(self):
        self.amount = 0
        self.rate = 0
        self.date = 0

# returns a boolean based on whether the csv file contains data
def dataExists(datePath, limit = 1):
    # opening the file
    file = open(datePath)
    data = csv.reader(file)

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
            divsplit = float(row[1])
            file.close()
            return divsplit

# returns the 10 year treasury note yield for stated month
def getNoteYield(date, datapath):
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
            rate = float(row[1])
            file.close()
            return rate
    


# returns the federal 2019 tax rate based on income
def fedTax(income):
    if income <= 9700:
        return .1
    elif income <= 39745:
        return .12
    elif income <= 84200:
        return .22
    elif income <= 160725:
        return .24
    elif income <= 204100:
        return .32
    elif income <= 510300:
        return .35
    else:
        return .37

# returns the federal 2019 tax rate for dividends
def divTax(bracket):
    if bracket <.25:
        return 0
    elif bracket < .35:
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
    return (eb**(1/n))/bb - 1

# returns the number of days between two dates
def diffDays(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    delta = d2 - d1
    return delta.days

# returns the number of months between two dates
def diffMonths(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    delta = d2 - d1
    return delta.months

# returns the percentage taxed as capital gains
def capitalGains(d1,d2, income):
    # get the number of the days between purchase and selling
    delta = diffDays(d1,d2)

    # if the stock has been held for less than a year
    if delta < 365:
        return fedTax(income)
    
    # if the stock has been for a year at least
    # return a tax bracket based on income
    else:
        if income <= 39375:
            return 0
        elif income <= 434550:
            return .15
        else:
            return .2

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
    movingAverageRows = [row for idx, row in enumerate(data) if idx in (index - period,index)]

    # calculate the current sum
    sum = 0
    for row in movingAverageRows:
        sum += float(row[4])
    
    # get the average
    SMA = sum/period

    file.close()
    
    return SMA


# returns data for the Buy and Hold strat
def BH(ticker, cash, income, commission):
    # initialize the data
    data = Data()
    data.type = "Buy and hold"

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
    for i in range(200):
        next(prices)

    # listify the csv file 
    prices = list(prices)
    
    # get the opening price for the 201st day
    price = float(prices[0][1])
    
    # get the current date and record it in the data
    date = prices[0][0]
    data.iDate = date

    # get the quantity of how many stocks you can buy
    quantity = math.floor(cash/price)

    # subtract the amount that I bought from the cash
    cash -= price * quantity

    # store in the information in a stock lot
    slot = Slot()
    slot.price = price
    slot.quantity = quantity
    slot.date = date

    # for every price, check to see if there was a stock split or a dividend issued
    for i in range(1, len(prices)):
        # if there is any data for splitting stocks
        if dataExists(splitPath):
            # if any of the dates appear in the stock split data
            if timeExists(prices[i][0],splitPath):
                # get the fraction of splitting
                fraction = getDivSplit(prices[i][0], splitPath)
                slot.quantity = math.floor(slot.quantity / fraction)
        
        # if there is any data for dividends
        if dataExists(divPath):
            # if any of the dates appear in the dividend data
            if timeExists(prices[i][0], divPath):
                # get the dividend for the day and calculate the money gained
                d = getDivSplit(prices[i][0], divPath)
                cash += d * slot.quantity * (1 - divTax(fedTax(income)))

                # record the dividends into data
                data.div += d * slot.quantity * (1 - divTax(fedTax(income)))

                # record the taxes paid
                data.taxes += d * slot.quantity * divTax(fedTax(income))
    
    # calculate profit/loss
    data.pl = (float(prices[-1][4]) - slot.price) * slot.quantity

    # calculate total assets
    data.assets = cash + (float(prices[-1][4]) * slot.quantity)

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[-1][0])

    # record the last date
    data.pDate = prices[-1][0]

    # close file
    priceF.close()

    return data



def MT(ticker, cash, income, baseSMA, commission):
    # initialize the data
    data = Data()
    data.type = "Momentum trading"

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
    for i in range(199):
        next(prices)
    
    # listify the csv.reader file
    prices = list(prices)

    # calculate the current moving average
    sma = movingAverage(baseSMA, prices[0][0], pricePath)

    # initialize the stock and note lots
    slot = Slot()
    nlot = Nlot()

    # get the current date and record it in the data
    date = prices[0][0]
    data.iDate = date
    
    # get the current month
    currD = prices[i][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    month = currD.month

    # if the closing price of the previous day is greater than or equal to the sma
    if float(prices[0][4]) >= sma:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # buy the stock at the current price
        slot.price = float(prices[1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[1][0]
        
        # subtract the amount used
        cash -= slot.price * slot.quantity


        # mark the boolean for keeping track of whether stocks or bonds have been bought
        boughtStock = True
    
    # if the current opening price is less than the sma
    else:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # buy treasury notes
        nlot.rate = getNoteYield(prices[1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[1][0]

        boughtStock = False


    # for every remaining price data
    for i in range(1, len(prices)):
        # calculate the current moving average
        sma = movingAverage(baseSMA, prices[i][0], pricePath)

        # get the current date
        currentDate = prices[i][0]
        currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

        # check if the current month is a different month compared to the last date
        if month != currentDate.month:
            month = currentDate.month
            checked = False

        # if the current date is after the tenth and stocks have not been checked
        # for this current month yet
        if currentDate.day >= 10 and checked == False:
            # set checked boolean to true
            checked = True

            # if the current closing price is less than the sma
            if float(prices[i][4]) < sma:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    stockEarnings = prices[i+1][1] * slot.quantity

                    # calculate capital gains tax
                    gainsTax = capitalGains(slot.date, prices[i+1][0], income)
                    
                    # account for taxes
                    stockEarnings *= 1-gainsTax
                    data.taxes += stockEarnings*gainsTax

                    # account for comissions
                    stockEarnings -= commission*2
                    data.comissions += commission*2

                    # account for the profit/loss
                    data.pl += (prices[i+1][1] - slot.price) * slot.quantity
                    cash += stockEarnings

                    # reset the slot
                    slot.price = 0
                    slot.quantity = 0
                    slot.date = 0

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    note.date = prices[i+1][0]

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # if it has been 6 months since the last purchase/payment
                    if diffMonths(prices[i][0], nlot.date) % 6 == 0:
                        cash += nlot.amount * (nlot.rate/100/2)
            
            # if the current closing price is greater than the sma
            else:
                # and if stocks were not bought and there are enough data points to gather data from
                if boughtStock == False and i+1 < len(prices):
                    # convert treasury yields into cash
                    cash += nlot.amount

                    # reset the nlot
                    nlot.amount = 0
                    nlot.date = 0
                    nlot.rate = 0

                    # account for comissions
                    stockEarnings -= commission*2
                    data.comissions += commission*2

                    # buy the stock at the current price
                    slot.price = prices[i+1][1]
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True

                # if stocks were bought and the current closing price is greater than or equal to the sma
                else:
                    # if there is any data for splitting stocks
                    if dataExists(splitPath):
                        # if any of the dates appear in the stock split data
                        if timeExists(prices[i][0],splitPath):
                            # get the fraction of splitting
                            fraction = getDivSplit(prices[i][0], splitPath)
                            slot.quantity = math.floor(slot.quantity / fraction)
                    
                    # if there is any data for dividends
                    if dataExists(divPath):
                        # if any of the dates appear in the dividend data
                        if timeExists(prices[i][0], divPath):
                            # get the dividend for the day and calculate the money gained
                            d = getDivSplit(prices[i][0], divPath)
                            cash += d * slot.quantity * (1 - divTax(fedTax(income)))

                            # record the dividends into data
                            data.div += d * slot.quantity * (1 - divTax(fedTax(income)))

                            # record the taxes paid
                            data.taxes += d * slot.quantity * divTax(fedTax(income))

    if boughtStock == True:
        # calculate profit/loss
        data.pl += (float(prices[-1][4]) - slot.price) * slot.quantity

        # calculate total assets
        data.assets = cash + (float(prices[-1][4]) * slot.quantity)
    
    else:
        # calculate total assets
        data.assets = cash + nlot.amount

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[-1][0])
    
    # record the last date
    data.pDate = prices[-1][0]

    # close file
    priceF.close()

    return data

# prints results from testing
def printResults(data1, data2):
    print("From " + data1.iDate + " to " + data1.pDate + " the strategies " + data1.type + " and " + data2.type + " were compared:")
    print("with a starting value of $" + str(data1.initial) + "...")
    print(data1.type + " strategy had a final value of $" + str(data1.assets) + " with a profit/loss of $" + str(data1.pl))
    print("A total of $" + str(data1.div) + " was paid in dividends.")
    print("A total of $" + str(data1.taxes) + " was paid in taxes.")
    print("A total of $" + str(data1.comissions) + " was paid in comissions.")
    print(data1.type + " strategy had a compound annual growth rate of " + str(data1.cagr))
    print(" ")
    print(data2.type + " strategy had a final value of $" + str(data2.assets) + " with a profit/loss of $" + str(data2.pl))
    print("A total of $" + str(data2.div) + " was paid in dividends.")
    print("A total of $" + str(data2.taxes) + " was paid in taxes.")
    print("A total of $" + str(data2.comissions) + " was paid in comissions.")
    print(data2.type + " strategy had a compound annual growth rate of " + str(data2.cagr))



def investCalc(ticker, initial, income, strat, baseSMA = 200, commission = 5):
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
            MTdata = MT(ticker, initial, income, baseSMA, commission)
            BHdata = BH(ticker, initial, income, commission)
            printResults(BHdata, MTdata)
        
        # elif strat == "GX":
        #     GXdata = GX()
        #     BHdata = BH()
        
        # elif strat == "DMT":
        
        # elif strat == "PMT":

        # elif strat == "GPM":

        # elif strat == "GDM":

        else:
            print("strategy does not exist, please input a valid strategy")


    else:
        print("Stock data does not have enough data points for this baseSMA")

    




# calculate buying and selling

# disclaimer about how the current model doesn't use historical data on tax rates
# disclaimer about how the current model doesn't use historical capital gains tax rates 

investCalc("SPY", 100000, 100000, "MT", 200, 5)