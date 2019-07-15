#!/usr/bin/env python

#investCalc by ComradeAkko

from priceExtractor import getTreasuryData, getStockData, newStockDirectory, newTreasuryDirectory
from datetime import datetime
import csv, operator
import math

# Classes:

# stores data for easy returning of data
class Data:
    def __init__(self, otherData):
        self.assets = 0
        self.cagr = 0
        self.taxes = 0
        self.comissions = 0
        self.pl = 0

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

# calculates compound annual growth rate
def cagr(bb, eb, n):
    return (eb^(1/n))/bb - 1

# calculates the current moving average based on the period
# and the current date
def movingAverage(period, date, dataPath):
    # get the csv file
    data = csv.reader(open(dataPath))
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
    
    return SMA


# returns data for the Buy and Hold strat
def BH(ticker, baseSMA, cash, commission):
    # initialize the data
    data = Data()

    # account for comissions
    cash -= commission
    data.comissions += commission

    #create the file path
    pricePath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker + "_price.csv"
    
    # get the csv file
    prices = csv.reader(open(pricePath))

    #skip the first 200 days
    for i in range(200)
        next(prices)

        # use a queue?
            #queue allows for a 

        # use the function?
    

    




def MT(ticker, baseSMA, cash, commission):

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
    priceData = csv.reader(open(stockPricePath), delimiter = ',')

    # counting the number of data points available
    rowCount = sum(1 for row in priceData)

    # if the there are enough data points for the SMA being used
    if rowCount > baseSMA:
        if strat == "MT":
            MTdata = MT(ticker, baseSMA, commission)
            BHdata = BH(ticker, baseSMA, commission)
        
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

    



# calculate 200 day moving average
# calculate 50 day moving average
# calculate buying and selling

# rename bonds to notes
# disclaimer about how the current model doesn't use historical data on tax rates
# disclaimer about how the current model doesn't use historical capital gains tax rates 