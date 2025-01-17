#!/usr/bin/env python

#investCalc by ComradeAkko

from priceExtractor import *
from datetime import datetime
from helperFunc import *
import csv, operator, math, os


# Classes:

# stores results data for later use
class Result:
    def __init__(self):
        self.ticker = 0
        self.strat1 = 0
        self.strat2 = 0
        self.strat3 = 0
        self.income = 0
        self.errorBoo = False
        self.errorMess = "nothing"

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
        self.treasury = 0
        self.iDate = 0
        self.pDate = 0
        self.income = 0

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

# returns data for the Buy and Hold strat
def BH(ticker, startDate, endDate, cash, income, baseSMA, commission):
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

    # listify the csv file 
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)
    
    # get the opening price for the baseSMA+1st day
    price = float(prices[startIDX][1])
    
    # get the current date and record it in the data
    date = prices[startIDX][0]
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
    for i in range(startIDX, endIDX+1):
        # if any of the dates appear in the stock split data
        if timeExists(prices[i][0],splitPath):
            # get the fraction of splitting
            fraction = getDivSplit(prices[i][0], splitPath)
            slot.quantity = math.floor(slot.quantity / fraction)
        
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
    data.pl = (float(prices[endIDX][4]) - slot.price) * slot.quantity

    # calculate total assets
    data.assets = cash + (float(prices[endIDX][4]) * slot.quantity)

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])

    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data



def MT(ticker, startDate, endDate, cash, income, baseSMA, commission):
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

    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # calculate the current moving average
    sma = movingAverage(baseSMA, prices[startIDX][0], pricePath)

    # initialize the stock and note lots
    slot = Slot()
    nlot = Nlot()

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    month = currD.month

    # set check boolean to true
    checked = True

    # if the closing price of the previous day is greater than or equal to the sma
    if float(prices[startIDX][4]) >= sma:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # buy the stock at the current price
        slot.price = float(prices[startIDX+1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[startIDX+1][0]
        
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
        nlot.rate = getNoteYield(prices[startIDX+1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[startIDX+1][0]

        boughtStock = False


    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
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

            # calculate the current moving average
            sma = movingAverage(baseSMA, prices[i][0], pricePath)

            # if the current closing price is less than the sma
            if float(prices[i][4]) < sma:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    # calculate value of stocks sold
                    stockEarnings = float(prices[i+1][1]) * slot.quantity

                    # calculate profit/loss
                    pl = (float(prices[i+1][1]) - slot.price) * slot.quantity

                    # if there is a technical profit (not including commission)
                    if pl > 0:
                        # calculate capital gains tax
                        gainsTax = capitalGains(slot.date, prices[i+1][0], income)

                        # account for taxes
                        paidTax = pl*gainsTax
                        data.taxes += paidTax
                        pl = pl*(1-gainsTax)

                        # subtract taxes from stock earnings
                        stockEarnings -= paidTax

                    # account for comissions
                    stockEarnings -= commission*2
                    data.comissions += commission*2

                    # account for the profit/loss
                    data.pl += pl
                    cash += stockEarnings

                    # reset the slot
                    slot.price = 0
                    slot.quantity = 0
                    slot.date = 0

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # if it has been 6 months since the last purchase/payment
                    if diffMonths(prices[i][0], nlot.date) % 6 == 0:
                        cash += nlot.amount * (nlot.rate/100/2)
                        data.treasury += nlot.amount * (nlot.rate/100/2)
            
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
                    cash -= commission*2
                    data.comissions += commission*2

                    # buy the stock at the current price
                    slot.price = float(prices[i+1][1])
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[i+1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True

        # if stocks were bought
        if boughtStock:
            # if any of the dates appear in the stock split data
            if timeExists(prices[i][0],splitPath):
                # get the fraction of splitting
                fraction = getDivSplit(prices[i][0], splitPath)
                slot.quantity = math.floor(slot.quantity / fraction)
                    
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
        data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity

        # calculate total assets
        data.assets = cash + (float(prices[endIDX][4]) * slot.quantity)
    
    else:
        # calculate total assets
        data.assets = cash + nlot.amount

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data

def GX(ticker, startDate, endDate, cash, income, baseSMA, commission):
    # initialize the data
    data = Data()
    data.type = "Golden Cross Momentum trading"

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
    
    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # calculate the current moving averages
    smaG = movingAverage(baseSMA, prices[startIDX][0], pricePath)
    smaL = movingAverage(math.floor(baseSMA/4), prices[startIDX][0], pricePath)

    # initialize the stock and note lots
    slot = Slot()
    nlot = Nlot()

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    month = currD.month

    # set check boolean to true
    checked = True

    # if the lesser day moving average is greater than or equat to the greater day moving average
    if smaL >= smaG:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # buy the stock at the current price
        slot.price = float(prices[startIDX+1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[startIDX+1][0]
        
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
        nlot.rate = getNoteYield(prices[startIDX+1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[startIDX+1][0]

        boughtStock = False


    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
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

            # calculate the current moving averages
            smaG = movingAverage(baseSMA, prices[i][0], pricePath)
            smaL = movingAverage(math.floor(baseSMA/4), prices[i][0], pricePath)

            # if the current lesser day moving average is lower than the greater day moving average
            if smaL < smaG:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    # calculate value of stocks sold
                    stockEarnings = float(prices[i+1][1]) * slot.quantity

                    # calculate profit/loss
                    pl = (float(prices[i+1][1]) - slot.price) * slot.quantity

                    # if there is a technical profit (not including commission)
                    if pl > 0:
                        # calculate capital gains tax
                        gainsTax = capitalGains(slot.date, prices[i+1][0], income)

                        # account for taxes
                        paidTax = pl*gainsTax
                        data.taxes += paidTax
                        pl = pl*(1-gainsTax)

                        # subtract taxes from stock earnings
                        stockEarnings -= paidTax

                    # account for comissions
                    stockEarnings -= commission*2
                    data.comissions += commission*2

                    # account for the profit/loss
                    data.pl += pl
                    cash += stockEarnings

                    # reset the slot
                    slot.price = 0
                    slot.quantity = 0
                    slot.date = 0

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # if it has been 6 months since the last purchase/payment
                    if diffMonths(prices[i][0], nlot.date) % 6 == 0:
                        cash += nlot.amount * (nlot.rate/100/2)
                        data.treasury += nlot.amount * (nlot.rate/100/2)
            
            # if the current lesser day moving average is greater than or equal to the greater day moving average
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
                    cash -= commission*2
                    data.comissions += commission*2

                    # buy the stock at the current price
                    slot.price = float(prices[i+1][1])
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[i+1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True

        # if stocks were bought
        if boughtStock:
            # if any of the dates appear in the stock split data
            if timeExists(prices[i][0],splitPath):
                # get the fraction of splitting
                fraction = getDivSplit(prices[i][0], splitPath)
                slot.quantity = math.floor(slot.quantity / fraction)
                    
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
        data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity

        # calculate total assets
        data.assets = cash + (float(prices[endIDX][4]) * slot.quantity)
    
    else:
        # calculate total assets
        data.assets = cash + nlot.amount

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data

def DCA(ticker, startDate, endDate, cash, income, baseSMA, commission, aigr, investFrac):
    # initialize the data
    data = Data()
    data.type = "Dollar Cost Averaging"

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
    
    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # initialize the stock lot list
    slotList = []

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month and year
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    year = currD.year
    month = currD.month

    # buy the intial lot of stocks
    # account for comissions
    cash -= commission
    data.comissions += commission

    # initialize the stock and lot
    slot = Slot()

    # buy the stock at the current price
    slot.price = float(prices[startIDX+1][1])
    slot.quantity = math.floor(cash/slot.price)
    slot.date = prices[startIDX+1][0]
    
    # subtract the amount used
    cash -= slot.price * slot.quantity

    # append the stock lot into the list
    slotList.append(slot)

    # set spending limits for this year
    budget = income*investFrac/12

    # set checked boolean to true
    checked = True

    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
        # get the current date
        currentDate = prices[i][0]
        currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

        # check if the current year is a different year compared to the last date
        if year != currentDate.year:
            year = currentDate.year

            # update the current income
            income *= 1+aigr

            # set spending limits for this year
            budget = (income*investFrac)/12

        # check if the current month is a different month compared to the last date
        if month != currentDate.month:
            month = currentDate.month
            checked = False

            # add the monthly budget of this year to cash
            cash += budget

        # if the current date is after the tenth and stocks have not been checked
        # for this current month yet
        if currentDate.day >= 10 and checked == False:
            # set checked boolean to true
            checked = True

            # check the stock's current price
            currPrice = float(prices[i+1][1])
            currQuantity = math.floor((cash-commission)/currPrice)

            # if there is enough money to buy at least one stock,
            # buy as many stock as possible
            if currQuantity > 0:
                slotNew = Slot()
                slotNew.price = currPrice
                slotNew.quantity = currQuantity
                slotNew.date = prices[i+1][0]

                # subtract the amount used
                cash -= slotNew.price * slotNew.quantity

                # account for comissions
                cash -= commission
                data.comissions += commission

                # add the current stockLot to the list of stock lot
                slotList.append(slotNew)

        # if any of the dates appear in the stock split data
        if timeExists(prices[i][0],splitPath):
            # get the fraction of splitting
            fraction = getDivSplit(prices[i][0], splitPath)

            # apply the split to all stock lots
            for lot in slotList:
                lot.quantity = math.floor(lot.quantity / fraction)
                    
        # if any of the dates appear in the dividend data
        if timeExists(prices[i][0], divPath):
            # get the dividend for the day and calculate the money gained
            d = getDivSplit(prices[i][0], divPath)
            
            # apply the dividend to all stock lots
            for lot in slotList:
                cash += d * lot.quantity * (1 - divTax(fedTax(income)))
                # record the dividends into data
                data.div += d * lot.quantity * (1 - divTax(fedTax(income)))

                # record the taxes paid
                data.taxes += d * lot.quantity * divTax(fedTax(income))
    
    # while there are slots to get from the stock list
    while slotList:
        # get a slot
        slot = slotList.pop()

        # add the profit/loss and total assets to the data
        data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity
        data.assets += float(prices[endIDX][4]) * slot.quantity
        
    # add the remaining cash to total assets
    data.assets += cash
    
    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data


def PMT(ticker, startDate, endDate, cash, income, baseSMA, commission, aigr, investFrac):
    # initialize the data
    data = Data()
    data.type = "Parallel Momentum trading"

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
    
    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # calculate the current moving average
    sma = movingAverage(baseSMA, prices[startIDX][0], pricePath)
    
    # initialize the stock and treasury note lot list
    slotList = []
    nlotList = []

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month and year
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    year = currD.year
    month = currD.month

    # set check boolean to true
    checked = True

    # set spending limits for this year
    budget = income*investFrac/12

    # if the closing price of the previous day is greater than or equal to the sma
    if float(prices[startIDX][4]) >= sma:
        # initialize the stock lot
        slot = Slot()

        # buy the stock at the current price
        slot.price = float(prices[startIDX+1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[startIDX+1][0]
    
        # subtract the amount used
        cash -= slot.price * slot.quantity

        # append the stock lot into the list
        slotList.append(slot)

        # mark the boolean for keeping track of whether stocks or bonds have been bought
        boughtStock = True
    
    # if the current opening price is less than the sma
    else:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # initialize the treasury note lot
        nlot = Nlot()

        # buy treasury notes
        nlot.rate = getNoteYield(prices[startIDX+1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[startIDX+1][0]

        # subtract the amount put into treasury notes from cash
        cash -= nlot.amount 

        # append treasury note lot to treasury note list
        nlotList.append(nlot)

        # set boolean 
        boughtStock = False

    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
        # get the current date
        currentDate = prices[i][0]
        currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

        # check if the current year is a different year compared to the last date
        if year != currentDate.year:
            year = currentDate.year

            # update the current income
            income *= 1+aigr

            # set spending limits for this year
            budget = income*investFrac/12

        # check if the current month is a different month compared to the last date
        if month != currentDate.month:
            month = currentDate.month
            checked = False

            # add the monthly budget of this year to cash
            cash += budget

        # if the current date is after the tenth and stocks have not been checked
        # for this current month yet
        if currentDate.day >= 10 and checked == False:
            # set checked boolean to true
            checked = True

            # calculate the current moving average
            sma = movingAverage(baseSMA, prices[i][0], pricePath)

            # if the current closing price is less than the sma
            if float(prices[i][4]) < sma:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    while slotList:
                        slot = slotList.pop()
                        # calculate value of stocks sold
                        stockEarnings = float(prices[i+1][1]) * slot.quantity

                        # calculate profit/loss
                        pl = (float(prices[i+1][1]) - slot.price) * slot.quantity

                        # if there is a technical profit (not including commission)
                        if pl > 0:
                            # calculate capital gains tax
                            gainsTax = capitalGains(slot.date, prices[i+1][0], income)

                            # account for taxes
                            paidTax = pl*gainsTax
                            data.taxes += paidTax
                            pl = pl*(1-gainsTax)

                            # subtract taxes from stock earnings
                            stockEarnings -= paidTax

                        # account for the profit/loss
                        data.pl += pl
                        cash += stockEarnings
                    
                    # account for commissions
                    cash -= commission*2
                    data.comissions += commission*2

                    # initialize the treasury note lot
                    nlot = Nlot()

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # add the treasury note to note list
                    nlotList.append(nlot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # for every treasury lot currently owned
                    for lot in nlotList:
                        # if it has been 6 months since the last purchase/payment
                        if diffMonths(prices[i][0], lot.date) % 6 == 0:
                            cash += lot.amount * (lot.rate/100/2)
                            data.treasury += lot.amount * (lot.rate/100/2)
                    
                    # account for commissions
                    cash -= commission
                    data.comissions += commission
                    
                    # convert the current cash to treasury bonds
                    nlot = Nlot()
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # add the treasury note to note list
                    nlotList.append(nlot)
            
                    
            # if the current closing price is greater than the sma
            else:
                # and if stocks were not bought and there are enough data points to gather data from
                if boughtStock == False and i+1 < len(prices):
                    # for every treasury note currently owned
                    while nlotList:
                        nlot = nlotList.pop()

                        # convert treasury notes into cash
                        cash += nlot.amount

                        # account for commissions
                        cash -= commission
                        data.comissions += commission

                    # account for comissions
                    cash -= commission
                    data.comissions += commission

                    # initialize another stock lot
                    slot = Slot()

                    # buy the stock at the current price
                    slot.price = float(prices[i+1][1])
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[i+1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # add the stock lot to the stock lot list
                    slotList.append(slot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True

                # and if stocks are already bought, buy more with the remaining cash
                elif i+1 < len(prices):
                    # check the stock's current price
                    currPrice = float(prices[i+1][1])
                    currQuantity = math.floor((cash-commission)/currPrice)

                    # if there is enough money to buy at least one stock,
                    # buy as many stock as possible
                    if currQuantity > 0:
                        slotNew = Slot()
                        slotNew.price = currPrice
                        slotNew.quantity = currQuantity
                        slotNew.date = prices[i+1][0]

                        # subtract the amount used
                        cash -= slotNew.price * slotNew.quantity

                        # account for comissions
                        cash -= commission
                        data.comissions += commission

                        # add the current stockLot to the list of stock lot
                        slotList.append(slotNew)

        # if stocks were bought
        if boughtStock:
            # if any of the dates appear in the stock split data
            if timeExists(prices[i][0],splitPath):
                # get the fraction of splitting
                fraction = getDivSplit(prices[i][0], splitPath)

                # apply the split to all stock lots
                for lot in slotList:
                    lot.quantity = math.floor(lot.quantity / fraction)
                        
            # if any of the dates appear in the dividend data
            if timeExists(prices[i][0], divPath):
                # get the dividend for the day and calculate the money gained
                d = getDivSplit(prices[i][0], divPath)
                
                # apply the dividend to all stock lots
                for lot in slotList:
                    cash += d * lot.quantity * (1 - divTax(fedTax(income)))
                    # record the dividends into data
                    data.div += d * lot.quantity * (1 - divTax(fedTax(income)))

                    # record the taxes paid
                    data.taxes += d * lot.quantity * divTax(fedTax(income))
    
    if boughtStock:
        # while there are slots to get from the stock list
        while slotList:
            # get a slot
            slot = slotList.pop()

            # add the profit/loss and total assets to the data
            data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity
            data.assets += float(prices[endIDX][4]) * slot.quantity
        
        # add the remaining cash to total assets
        data.assets += cash
        
    else:
        # while there are slots to get from the treasury list
        while nlotList:
            # get a slot
            nlot = nlotList.pop()

            data.assets += nlot.amount
        # add the remaining cash to total assets
        data.assets += cash

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data

def DMT(ticker, startDate, endDate, cash, income, baseSMA, commission, aigr, investFrac):
    # initialize the data
    data = Data()
    data.type = "Divergent Momentum trading"

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
    
    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # calculate the current moving average
    sma = movingAverage(baseSMA, prices[startIDX][0], pricePath)
    
    # initialize the stock and treasury note lot list
    slotList = []
    nlotList = []

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month and year
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    year = currD.year
    month = currD.month

    # set check boolean to true
    checked = True

    # set spending limits for this year
    budget = income*investFrac/12

    # if the closing price of the previous day is greater than or equal to the sma
    if float(prices[startIDX][4]) >= sma:
        # initialize the stock lot
        slot = Slot()

        # buy the stock at the current price
        slot.price = float(prices[startIDX+1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[startIDX+1][0]
    
        # subtract the amount used
        cash -= slot.price * slot.quantity

        # append the stock lot into the list
        slotList.append(slot)

        # mark the boolean for keeping track of whether stocks or bonds have been bought
        boughtStock = True
    
    # if the current opening price is less than the sma
    else:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # initialize the treasury note lot
        nlot = Nlot()

        # buy treasury notes
        nlot.rate = getNoteYield(prices[startIDX+1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[startIDX+1][0]

        # subtract the amount put into treasury notes from cash
        cash -= nlot.amount 

        # append treasury note lot to treasury note list
        nlotList.append(nlot)

        # set boolean 
        boughtStock = False

    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
        # get the current date
        currentDate = prices[i][0]
        currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

        # check if the current year is a different year compared to the last date
        if year != currentDate.year:
            year = currentDate.year

            # update the current income
            income *= 1+aigr

            # set spending limits for this year
            budget = income*investFrac/12

        # check if the current month is a different month compared to the last date
        if month != currentDate.month:
            month = currentDate.month
            checked = False

            # add the monthly budget of this year to cash
            cash += budget

        # if the current date is after the tenth and stocks have not been checked
        # for this current month yet
        if currentDate.day >= 10 and checked == False:
            # set checked boolean to true
            checked = True

            # calculate the current moving average
            sma = movingAverage(baseSMA, prices[i][0], pricePath)

            # if the current closing price is less than the sma
            if float(prices[i][4]) < sma:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    while slotList:
                        slot = slotList.pop()
                        # calculate value of stocks sold
                        stockEarnings = float(prices[i+1][1]) * slot.quantity

                        # calculate profit/loss
                        pl = (float(prices[i+1][1]) - slot.price) * slot.quantity

                        # if there is a technical profit (not including commission)
                        if pl > 0:
                            # calculate capital gains tax
                            gainsTax = capitalGains(slot.date, prices[i+1][0], income)

                            # account for taxes
                            paidTax = pl*gainsTax
                            data.taxes += paidTax
                            pl = pl*(1-gainsTax)

                            # subtract taxes from stock earnings
                            stockEarnings -= paidTax

                        # account for the profit/loss
                        data.pl += pl
                        cash += stockEarnings
                    
                    # account for commissions
                    cash -= commission*2
                    data.comissions += commission*2

                    # initialize the treasury note lot
                    nlot = Nlot()

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # add the treasury note to note list
                    nlotList.append(nlot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # for every treasury lot currently owned
                    for lot in nlotList:
                        # if it has been 6 months since the last purchase/payment
                        if diffMonths(prices[i][0], lot.date) % 6 == 0:
                            cash += lot.amount * (lot.rate/100/2)
                            data.treasury += lot.amount * (lot.rate/100/2)
                    
                    # if there are enough data points left
                    if i+1 < len(prices):
                        # check the stock's current price
                        currPrice = float(prices[i+1][1])
                        currQuantity = math.floor((cash-commission)/currPrice)

                        # if there is enough money to buy at least one stock,
                        # buy as many stock as possible
                        if currQuantity > 0:
                            slotNew = Slot()
                            slotNew.price = currPrice
                            slotNew.quantity = currQuantity
                            slotNew.date = prices[i+1][0]

                            # subtract the amount used
                            cash -= slotNew.price * slotNew.quantity

                            # account for comissions
                            cash -= commission
                            data.comissions += commission

                            # add the current stockLot to the list of stock lot
                            slotList.append(slotNew)
            
                    
            # if the current closing price is greater than the sma
            else:
                # and if stocks were not bought and there are enough data points to gather data from
                if boughtStock == False and i+1 < len(prices):
                    # for every treasury note currently owned
                    while nlotList:
                        nlot = nlotList.pop()

                        # convert treasury notes into cash
                        cash += nlot.amount

                        # account for commissions
                        cash -= commission
                        data.comissions += commission

                    # account for comissions
                    cash -= commission
                    data.comissions += commission

                    # initialize another stock lot
                    slot = Slot()

                    # buy the stock at the current price
                    slot.price = float(prices[i+1][1])
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[i+1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # add the stock lot to the stock lot list
                    slotList.append(slot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True
                # and if stocks are already bought, buy more with the remaining cash
                elif i+1 < len(prices):
                    # check the stock's current price
                    currPrice = float(prices[i+1][1])
                    currQuantity = math.floor((cash-commission)/currPrice)

                    # if there is enough money to buy at least one stock,
                    # buy as many stock as possible
                    if currQuantity > 0:
                        slotNew = Slot()
                        slotNew.price = currPrice
                        slotNew.quantity = currQuantity
                        slotNew.date = prices[i+1][0]

                        # subtract the amount used
                        cash -= slotNew.price * slotNew.quantity

                        # account for comissions
                        cash -= commission
                        data.comissions += commission

                        # add the current stockLot to the list of stock lot
                        slotList.append(slotNew)

        # if any of the dates appear in the stock split data
        if timeExists(prices[i][0],splitPath):
            # get the fraction of splitting
            fraction = getDivSplit(prices[i][0], splitPath)

            # apply the split to all stock lots
            for lot in slotList:
                lot.quantity = math.floor(lot.quantity / fraction)
                        
        # if any of the dates appear in the dividend data
        if timeExists(prices[i][0], divPath):
            # get the dividend for the day and calculate the money gained
            d = getDivSplit(prices[i][0], divPath)
                
            # apply the dividend to all stock lots
            for lot in slotList:
                cash += d * lot.quantity * (1 - divTax(fedTax(income)))
                # record the dividends into data
                data.div += d * lot.quantity * (1 - divTax(fedTax(income)))

                # record the taxes paid
                data.taxes += d * lot.quantity * divTax(fedTax(income))
    
    # while there are slots to get from the stock list
    while slotList:
        # get a slot
        slot = slotList.pop()

        # add the profit/loss and total assets to the data
        data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity
        data.assets += float(prices[endIDX][4]) * slot.quantity   

    # while there are slots to get from the treasury list
    while nlotList:
        # get a slot
        nlot = nlotList.pop()

        data.assets += nlot.amount
    # add the remaining cash to total assets
    data.assets += cash

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data

def GPM(ticker, startDate, endDate, cash, income, baseSMA, commission, aigr, investFrac):
    # initialize the data
    data = Data()
    data.type = "Golden Cross Parallel Momentum trading"

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
    
    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # calculate the current moving averages
    smaG = movingAverage(baseSMA, prices[startIDX][0], pricePath)
    smaL = movingAverage(math.floor(baseSMA/4), prices[startIDX][0], pricePath)

    # initialize the stock and treasury note lot list
    slotList = []
    nlotList = []

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month and year
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    year = currD.year
    month = currD.month

    # set check boolean to true
    checked = True

    # set spending limits for this year
    budget = income*investFrac/12

    # if the closing price of the previous day is greater than or equal to the sma
    if smaL >= smaG:
        # initialize the stock lot
        slot = Slot()

        # buy the stock at the current price
        slot.price = float(prices[startIDX+1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[startIDX+1][0]
    
        # subtract the amount used
        cash -= slot.price * slot.quantity

        # append the stock lot into the list
        slotList.append(slot)

        # mark the boolean for keeping track of whether stocks or bonds have been bought
        boughtStock = True
    
    # if the current opening price is less than the sma
    else:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # initialize the treasury note lot
        nlot = Nlot()

        # buy treasury notes
        nlot.rate = getNoteYield(prices[startIDX+1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[startIDX+1][0]

        # subtract the amount put into treasury notes from cash
        cash -= nlot.amount 

        # append treasury note lot to treasury note list
        nlotList.append(nlot)

        # set boolean 
        boughtStock = False

    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
        # get the current date
        currentDate = prices[i][0]
        currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

        # check if the current year is a different year compared to the last date
        if year != currentDate.year:
            year = currentDate.year

            # update the current income
            income *= 1+aigr

            # set spending limits for this year
            budget = income*investFrac/12

        # check if the current month is a different month compared to the last date
        if month != currentDate.month:
            month = currentDate.month
            checked = False

            # add the monthly budget of this year to cash
            cash += budget

        # if the current date is after the tenth and stocks have not been checked
        # for this current month yet
        if currentDate.day >= 10 and checked == False:
            # set checked boolean to true
            checked = True

            # calculate the current moving averages
            smaG = movingAverage(baseSMA, prices[i][0], pricePath)
            smaL = movingAverage(math.floor(baseSMA/4), prices[i][0], pricePath)

            # if the current lesser SMA is less than the greater SMA
            if smaL < smaG:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    while slotList:
                        slot = slotList.pop()
                        # calculate value of stocks sold
                        stockEarnings = float(prices[i+1][1]) * slot.quantity

                        # calculate profit/loss
                        pl = (float(prices[i+1][1]) - slot.price) * slot.quantity

                        # if there is a technical profit (not including commission)
                        if pl > 0:
                            # calculate capital gains tax
                            gainsTax = capitalGains(slot.date, prices[i+1][0], income)

                            # account for taxes
                            paidTax = pl*gainsTax
                            data.taxes += paidTax
                            pl = pl*(1-gainsTax)

                            # subtract taxes from stock earnings
                            stockEarnings -= paidTax

                        # account for the profit/loss
                        data.pl += pl
                        cash += stockEarnings
                    
                    # account for commissions
                    cash -= commission*2
                    data.comissions += commission*2

                    # initialize the treasury note lot
                    nlot = Nlot()

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # add the treasury note to note list
                    nlotList.append(nlot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # for every treasury lot currently owned
                    for lot in nlotList:
                        # if it has been 6 months since the last purchase/payment
                        if diffMonths(prices[i][0], lot.date) % 6 == 0:
                            cash += lot.amount * (lot.rate/100/2)
                            data.treasury += lot.amount * (lot.rate/100/2)
                    
                    # account for commissions
                    cash -= commission
                    data.comissions += commission
                    
                    # convert the current cash to treasury bonds
                    nlot = Nlot()
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # add the treasury note to note list
                    nlotList.append(nlot)
            
                    
            # if the current closing price is greater than the sma
            else:
                # and if stocks were not bought and there are enough data points to gather data from
                if boughtStock == False and i+1 < len(prices):
                    # for every treasury note currently owned
                    while nlotList:
                        nlot = nlotList.pop()

                        # convert treasury notes into cash
                        cash += nlot.amount

                        # account for commissions
                        cash -= commission
                        data.comissions += commission

                    # account for comissions
                    cash -= commission
                    data.comissions += commission

                    # initialize another stock lot
                    slot = Slot()

                    # buy the stock at the current price
                    slot.price = float(prices[i+1][1])
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[i+1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # add the stock lot to the stock lot list
                    slotList.append(slot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True

                # and if stocks are already bought, buy more with the remaining cash
                elif i+1 < len(prices):
                    # check the stock's current price
                    currPrice = float(prices[i+1][1])
                    currQuantity = math.floor((cash-commission)/currPrice)

                    # if there is enough money to buy at least one stock,
                    # buy as many stock as possible
                    if currQuantity > 0:
                        slotNew = Slot()
                        slotNew.price = currPrice
                        slotNew.quantity = currQuantity
                        slotNew.date = prices[i+1][0]

                        # subtract the amount used
                        cash -= slotNew.price * slotNew.quantity

                        # account for comissions
                        cash -= commission
                        data.comissions += commission

                        # add the current stockLot to the list of stock lot
                        slotList.append(slotNew)

        # if stocks were bought
        if boughtStock:
            # if any of the dates appear in the stock split data
            if timeExists(prices[i][0],splitPath):
                # get the fraction of splitting
                fraction = getDivSplit(prices[i][0], splitPath)

                # apply the split to all stock lots
                for lot in slotList:
                    lot.quantity = math.floor(lot.quantity / fraction)
                        
            # if any of the dates appear in the dividend data
            if timeExists(prices[i][0], divPath):
                # get the dividend for the day and calculate the money gained
                d = getDivSplit(prices[i][0], divPath)
                
                # apply the dividend to all stock lots
                for lot in slotList:
                    cash += d * lot.quantity * (1 - divTax(fedTax(income)))
                    # record the dividends into data
                    data.div += d * lot.quantity * (1 - divTax(fedTax(income)))

                    # record the taxes paid
                    data.taxes += d * lot.quantity * divTax(fedTax(income))
    
    if boughtStock:
        # while there are slots to get from the stock list
        while slotList:
            # get a slot
            slot = slotList.pop()

            # add the profit/loss and total assets to the data
            data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity
            data.assets += float(prices[endIDX][4]) * slot.quantity
        
        # add the remaining cash to total assets
        data.assets += cash
        
    else:
        # while there are slots to get from the treasury list
        while nlotList:
            # get a slot
            nlot = nlotList.pop()

            data.assets += nlot.amount
        # add the remaining cash to total assets
        data.assets += cash

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data

def GDM(ticker, startDate, endDate, cash, income, baseSMA, commission, aigr, investFrac):
    # initialize the data
    data = Data()
    data.type = "Golden Cross Divergent Momentum trading"

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
    
    # listify the csv.reader file
    prices = list(prices)

    # get the index of the starting date:
    startIDX = binaryDateSearch(prices, 0, len(prices)-1, startDate)

    # get the index of the ending date:
    endIDX = binaryDateSearch(prices, 0, len(prices)-1, endDate)

    # calculate the current moving averages
    smaG = movingAverage(baseSMA, prices[startIDX][0], pricePath)
    smaL = movingAverage(math.floor(baseSMA/4), prices[startIDX][0], pricePath)

    # initialize the stock and treasury note lot list
    slotList = []
    nlotList = []

    # get the current date and record it in the data
    date = prices[startIDX][0]
    data.iDate = date
    
    # get the current month and year
    currD = prices[startIDX][0]
    currD = datetime.strptime(currD, "%Y-%m-%d")
    year = currD.year
    month = currD.month

    # set check boolean to true
    checked = True

    # set spending limits for this year
    budget = income*investFrac/12

    # if the lesser SMA is greater than or equal to the greater SMA
    if smaL >= smaG:
        # initialize the stock lot
        slot = Slot()

        # buy the stock at the current price
        slot.price = float(prices[startIDX+1][1])
        slot.quantity = math.floor(cash/slot.price)
        slot.date = prices[startIDX+1][0]
    
        # subtract the amount used
        cash -= slot.price * slot.quantity

        # append the stock lot into the list
        slotList.append(slot)

        # mark the boolean for keeping track of whether stocks or bonds have been bought
        boughtStock = True
    
    # if the current opening price is less than the sma
    else:
        # account for comissions
        cash -= commission
        data.comissions += commission

        # initialize the treasury note lot
        nlot = Nlot()

        # buy treasury notes
        nlot.rate = getNoteYield(prices[startIDX+1][0], notePath)
        nlot.amount = cash
        nlot.date = prices[startIDX+1][0]

        # subtract the amount put into treasury notes from cash
        cash -= nlot.amount 

        # append treasury note lot to treasury note list
        nlotList.append(nlot)

        # set boolean 
        boughtStock = False

    # for every remaining price data
    for i in range(startIDX+1, endIDX+1):
        # get the current date
        currentDate = prices[i][0]
        currentDate = datetime.strptime(currentDate, "%Y-%m-%d")

        # check if the current year is a different year compared to the last date
        if year != currentDate.year:
            year = currentDate.year

            # update the current income
            income *= 1+aigr

            # set spending limits for this year
            budget = income*investFrac/12

        # check if the current month is a different month compared to the last date
        if month != currentDate.month:
            month = currentDate.month
            checked = False

            # add the monthly budget of this year to cash
            cash += budget

        # if the current date is after the tenth and stocks have not been checked
        # for this current month yet
        if currentDate.day >= 10 and checked == False:
            # set checked boolean to true
            checked = True

            # calculate the current moving averages
            smaG = movingAverage(baseSMA, prices[i][0], pricePath)
            smaL = movingAverage(math.floor(baseSMA/4), prices[i][0], pricePath)

            # if the current lesser SMA is less than the greater SMA
            if smaL < smaG:
                # if stocks were bought and there is enough a data points to get a price to sell
                if boughtStock and i+1 < len(prices):
                    while slotList:
                        slot = slotList.pop()
                        # calculate value of stocks sold
                        stockEarnings = float(prices[i+1][1]) * slot.quantity

                        # calculate profit/loss
                        pl = (float(prices[i+1][1]) - slot.price) * slot.quantity

                        # if there is a technical profit (not including commission)
                        if pl > 0:
                            # calculate capital gains tax
                            gainsTax = capitalGains(slot.date, prices[i+1][0], income)

                            # account for taxes
                            paidTax = pl*gainsTax
                            data.taxes += paidTax
                            pl = pl*(1-gainsTax)

                            # subtract taxes from stock earnings
                            stockEarnings -= paidTax

                        # account for the profit/loss
                        data.pl += pl
                        cash += stockEarnings
                    
                    # account for commissions
                    cash -= commission*2
                    data.comissions += commission*2

                    # initialize the treasury note lot
                    nlot = Nlot()

                    # convert the cash to treasury note
                    nlot.amount = cash
                    cash -= nlot.amount
                    nlot.rate = getNoteYield(prices[i+1][0], notePath)
                    nlot.date = prices[i+1][0]

                    # add the treasury note to note list
                    nlotList.append(nlot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = False

                # if stocks were not bought and the current closing price is less than the sma
                else:
                    # for every treasury lot currently owned
                    for lot in nlotList:
                        # if it has been 6 months since the last purchase/payment
                        if diffMonths(prices[i][0], lot.date) % 6 == 0:
                            cash += lot.amount * (lot.rate/100/2)
                            data.treasury += lot.amount * (lot.rate/100/2)
                    
                    # if there are enough data points left
                    if i+1 < len(prices):
                        # check the stock's current price
                        currPrice = float(prices[i+1][1])
                        currQuantity = math.floor((cash-commission)/currPrice)

                        # if there is enough money to buy at least one stock,
                        # buy as many stock as possible
                        if currQuantity > 0:
                            slotNew = Slot()
                            slotNew.price = currPrice
                            slotNew.quantity = currQuantity
                            slotNew.date = prices[i+1][0]

                            # subtract the amount used
                            cash -= slotNew.price * slotNew.quantity

                            # account for comissions
                            cash -= commission
                            data.comissions += commission

                            # add the current stockLot to the list of stock lot
                            slotList.append(slotNew)
            
                    
            # if the current closing price is greater than the sma
            else:
                # and if stocks were not bought and there are enough data points to gather data from
                if boughtStock == False and i+1 < len(prices):
                    # for every treasury note currently owned
                    while nlotList:
                        nlot = nlotList.pop()

                        # convert treasury notes into cash
                        cash += nlot.amount

                        # account for commissions
                        cash -= commission
                        data.comissions += commission

                    # account for comissions
                    cash -= commission
                    data.comissions += commission

                    # initialize another stock lot
                    slot = Slot()

                    # buy the stock at the current price
                    slot.price = float(prices[i+1][1])
                    slot.quantity = math.floor(cash/slot.price)
                    slot.date = prices[i+1][0]

                    # subtract the amount used
                    cash -= slot.price * slot.quantity

                    # add the stock lot to the stock lot list
                    slotList.append(slot)

                    # mark the boolean for keeping track of whether stocks or bonds have been bought
                    boughtStock = True
                # and if stocks are already bought, buy more with the remaining cash
                elif i+1 < len(prices):
                    # check the stock's current price
                    currPrice = float(prices[i+1][1])
                    currQuantity = math.floor((cash-commission)/currPrice)

                    # if there is enough money to buy at least one stock,
                    # buy as many stock as possible
                    if currQuantity > 0:
                        slotNew = Slot()
                        slotNew.price = currPrice
                        slotNew.quantity = currQuantity
                        slotNew.date = prices[i+1][0]

                        # subtract the amount used
                        cash -= slotNew.price * slotNew.quantity

                        # account for comissions
                        cash -= commission
                        data.comissions += commission

                        # add the current stockLot to the list of stock lot
                        slotList.append(slotNew)

        # if any of the dates appear in the stock split data
        if timeExists(prices[i][0],splitPath):
            # get the fraction of splitting
            fraction = getDivSplit(prices[i][0], splitPath)

            # apply the split to all stock lots
            for lot in slotList:
                lot.quantity = math.floor(lot.quantity / fraction)
                        
        # if any of the dates appear in the dividend data
        if timeExists(prices[i][0], divPath):
            # get the dividend for the day and calculate the money gained
            d = getDivSplit(prices[i][0], divPath)
                
            # apply the dividend to all stock lots
            for lot in slotList:
                cash += d * lot.quantity * (1 - divTax(fedTax(income)))
                # record the dividends into data
                data.div += d * lot.quantity * (1 - divTax(fedTax(income)))

                # record the taxes paid
                data.taxes += d * lot.quantity * divTax(fedTax(income))
    
    # while there are slots to get from the stock list
    while slotList:
        # get a slot
        slot = slotList.pop()

        # add the profit/loss and total assets to the data
        data.pl += (float(prices[endIDX][4]) - slot.price) * slot.quantity
        data.assets += float(prices[endIDX][4]) * slot.quantity   

    # while there are slots to get from the treasury list
    while nlotList:
        # get a slot
        nlot = nlotList.pop()

        data.assets += nlot.amount
    # add the remaining cash to total assets
    data.assets += cash

    # calculate cagr
    data.cagr = cagr(data.initial, data.assets, data.iDate, prices[endIDX][0])
    
    # record the last date
    data.pDate = prices[endIDX][0]

    # record the final income
    data.income = income

    # close file
    priceF.close()

    return data

# prints 2 results from testing
def printResults2(ticker, data1, data2):
    print("The following results are based on the ticker: " + ticker)
    print("From " + data1.iDate + " to " + data1.pDate + " the strategies " + data1.type + " and " + data2.type + " were compared:")
    print("with a starting value of $" + str(data1.initial) + "...")
    print(data1.type + " strategy had a final value of $" + str(data1.assets) + " with a profit/loss of $" + str(data1.pl))
    print("A total of $" + str(data1.div) + " was paid in dividends.")
    print("A total of $" + str(data1.treasury) + " was paid in treasury yields.")
    print("A total of $" + str(data1.taxes) + " was paid in taxes.")
    print("A total of $" + str(data1.comissions) + " was paid in comissions.")
    print(data1.type + " strategy had a compound annual growth rate of " + str(data1.cagr))
    print(" ")
    print(data2.type + " strategy had a final value of $" + str(data2.assets) + " with a profit/loss of $" + str(data2.pl))
    print("A total of $" + str(data2.div) + " was paid in dividends.")
    print("A total of $" + str(data2.treasury) + " was paid in treasury yields.")
    print("A total of $" + str(data2.taxes) + " was paid in taxes.")
    print("A total of $" + str(data2.comissions) + " was paid in comissions.")
    print(data2.type + " strategy had a compound annual growth rate of " + str(data2.cagr))

# prints 3 results from testing
def printResults3(ticker, data1, data2, data3):
    print("The following results are based on the ticker: " + ticker)
    print("From " + data1.iDate + " to " + data1.pDate + " the strategies " + data1.type + ", " + data2.type + " and " + data3.type + " were compared:")
    print("with a starting value of $" + str(data1.initial) + "...")
    print(data1.type + " strategy had a final value of $" + str(data1.assets) + " with a profit/loss of $" + str(data1.pl))
    print("A total of $" + str(data1.div) + " was paid in dividends.")
    print("A total of $" + str(data1.treasury) + " was paid in treasury yields.")
    print("A total of $" + str(data1.taxes) + " was paid in taxes.")
    print("A total of $" + str(data1.comissions) + " was paid in comissions.")
    print(data1.type + " strategy had a compound annual growth rate of " + str(data1.cagr))
    print(" ")
    print(data2.type + " strategy had a final value of $" + str(data2.assets) + " with a profit/loss of $" + str(data2.pl))
    print("A total of $" + str(data2.div) + " was paid in dividends.")
    print("A total of $" + str(data2.treasury) + " was paid in treasury yields.")
    print("A total of $" + str(data2.taxes) + " was paid in taxes.")
    print("A total of $" + str(data2.comissions) + " was paid in comissions.")
    print(data2.type + " strategy had a compound annual growth rate of " + str(data2.cagr))
    print(" ")
    print(data3.type + " strategy had a final value of $" + str(data3.assets) + " with a profit/loss of $" + str(data3.pl))
    print("A total of $" + str(data3.div) + " was paid in dividends.")
    print("A total of $" + str(data3.treasury) + " was paid in treasury yields.")
    print("A total of $" + str(data3.taxes) + " was paid in taxes.")
    print("A total of $" + str(data3.comissions) + " was paid in comissions.")
    print(data3.type + " strategy had a compound annual growth rate of " + str(data3.cagr))

# InvestCalc():
# calculates how certain strategies do within a historical context
# ticker:       ticker of the stock being evaluated
#
# startDate:    the startDate of the calculations. If there is not enough data
#                   beforehand to calculate the baseSMA, the earliest date
#                   where the baseSMA can be calculated will be used instead.
#
#                   Dates should be inputted in "MM/DD/YYYY" format.
#
#                   If "MAX" is inputted, calculations will start at the earliest
#                   possible.
#
#
# endDate:      the endDate of the calculations. If there are not enough datapoints between
#                   the startDate and the endDate, an error will be shown.
#
#                   Dates should be inputted in "MM/DD/YYYY" format.
#
#                   If "MAX" is inputted, calculations will end at the latest
#                   date possible.
#
#
# initial:      the initial amount of capital to be used
#
# income:       the annual income of the person
#
# strat1:       the first strategy to be compared. Is necessary.
#
# strat2:       the second strategy to be compared. Is necessary.
#
# strat2:       the third strategy to be compared. Is not necessary. 
#
# baseSMA:      Base Simple Moving Average. Moving average base to be used in strategies.
#                   Set to 200 in default.
#                   In golden cross strategies where two SMA's are used, the lesser SMA
#                   will be the floor of baseSMA/4, so in default the lesser SMA is 50.
#
# investFrac:   Investment fraction. ONLY USED IN ACTIVE STRATEGIES. 
#                   Specifies what fraction of untaxed income will be used for investment purposes annually.
#                   Set to zero in default.
#                   Decimal should be inputted. (i.e. .8 for 80% or .15 for 15%)
#
# aigr:         Annual Income Growth Rate. ONLY USED IN ACTIVE STRATEGIES. 
#                   Specifies the annual growth rate of income.
#                   Set to zero in default.
#                   Decimal should be inputted. (i.e. .02 for 2%, .015 for 1.5%)

def investCalc(ticker, startDate, endDate, initial, income, strat1, strat2, strat3, baseSMA = 200, commission = 5, investFrac = 0, aigr = 0):
    # initialize the results
    results = Result()

    # turn ticker into upper case
    ticker = ticker.upper()
    results.ticker = ticker

    stockPath = os.getcwd() + "\\stocks\\" + ticker + "\\" + ticker
    notesPath = os.getcwd() + "\\notes\\notes.csv"
    tickerPath = os.getcwd() + "\\ticker\\"

    # make sure the initial capital is greater than zero
    if initial <= 0 or baseSMA <= 0:
        results.errorBoo = True
        results.errorMess = "Initial capital and/or baseSMA must be greater than zero"
        return results
    
    # make sure the income is not negative
    if income < 0:
        results.errorBoo = True
        results.errorMess = "Income cannot be negative"
        return results

    # make sure the investfrac is a decimal between zero and one
    if investFrac < 0 or investFrac > 1:
        results.errorBoo = True
        results.errorMess = "The fraction of income reserved for investing must not be beyond 0.0 and 1.0"
        return results

    # make sure the aigr is not lesser than -1.0
    if aigr < -1:
        results.errorBoo = True
        results.errorMess = "The annual income growth rate must not be lesser than -1.0"
        return results


    # make sure we have the files
    if os.path.isfile(tickerPath + "nasdaq.csv") == False or os.path.isfile(tickerPath + "nyse.csv") == False or os.path.isfile(tickerPath + "amex.csv") == False or  os.path.isfile(tickerPath + "etf.csv") == False:
        getTickerList()
    if os.path.isfile(notesPath) == False:
        getTreasuryData()

    # make sure the ticker exists
    if tickerExists(ticker):
        if os.path.isfile(stockPath + "_split.csv") == False or os.path.isfile(stockPath + "_price.csv") == False or os.path.isfile(stockPath + "_dividend.csv") == False:
            getStockData(ticker)
    # if the ticker does not exist, return error
    else:
        results.errorBoo = True
        results.errorMess = "Ticker does not exist in AMEX, ETFList(NASDAQ), NASDAQ, and NYSE"
        return results
    
    # getting the csv file
    stockPricePath = stockPath + "_price.csv"

    # if the there are enough data points for the SMA being used
    if dataExists(stockPricePath, baseSMA):
        # get the start and end dates
        startDate = getStartDate(stockPricePath, startDate, baseSMA)
        if startDate == False:
            results.errorBoo = True
            results.errorMess = "Start date is invalid"
            return results

        endDate = getEndDate(stockPricePath, endDate, baseSMA)
        if endDate == False:
            results.errorBoo = True
            results.errorMess = "End date is invalid"
            return results

        # if the startDate is properly earlier than the endDate
        if startDate < endDate:
            # booleans to determine if a strat has been found
            found1 = False
            found2 = False
            found3 = False

            # compare the strategies
            if strat1 == "BH" or strat2 == "BH" or strat3 == "BH":
                if strat1 == "BH":
                    data1 = BH(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found1 = True

                if strat2 == "BH":
                    data2 = BH(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found2 = True
                
                if strat3 == "BH":
                    data3 = BH(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found3 = True

            if strat1 == "MT" or strat2 == "MT" or strat3 == "MT":
                if strat1 == "MT":
                    data1 = MT(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found1 = True

                if strat2 == "MT":
                    data2 = MT(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found2 = True

                if strat3 == "MT":
                    data3 = MT(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found3 = True

            
            if strat1 == "GX" or strat2 == "GX" or strat3 == "GX":
                if strat1 == "GX":
                    data1 = GX(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found1 = True

                if strat2 == "GX":
                    data2 = GX(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found2 = True

                if strat3 == "GX":
                    data3 = GX(ticker, startDate, endDate, initial, income, baseSMA, commission)
                    found3 = True
            
            if strat1 == "DCA" or strat2 == "DCA" or strat3 == "DCA":
                if strat1 == "DCA":
                    data1 = DCA(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found1 = True

                if strat2 == "DCA":
                    data2 = DCA(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found2 = True
                
                if strat3 == "DCA":
                    data3 = DCA(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found3 = True
            
            if strat1 == "PMT" or strat2 == "PMT" or strat3 == "PMT":
                if strat1 == "PMT":
                    data1 = PMT(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found1 = True

                if strat2 == "PMT":
                    data2 = PMT(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found2 = True

                if strat3 == "PMT":
                    data3 = PMT(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found3 = True

            if strat1 == "DMT" or strat2 == "DMT" or strat3 == "DMT":
                if strat1 == "DMT":
                    data1 = DMT(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found1 = True

                if strat2 == "DMT":
                    data2 = DMT(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found2 = True

                if strat3 == "DMT":
                    data3 = DMT(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found3 = True    

            if strat1 == "GPM" or strat2 == "GPM" or strat3 == "GPM":
                if strat1 == "GPM":
                    data1 = GPM(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found1 = True

                if strat2 == "GPM":
                    data2 = GPM(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found2 = True

                if strat3 == "GPM":
                    data3 = GPM(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found3 = True
                
            if strat1 == "GDM" or strat2 == "GDM" or strat3 == "GDM":
                if strat1 == "GDM":
                    data1 = GDM(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found1 = True

                if strat2 == "GDM":
                    data2 = GDM(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found2 = True

                if strat3 == "GDM":
                    data3 = GDM(ticker, startDate, endDate, initial, income, baseSMA, commission, aigr, investFrac)
                    found3 = True

            # return the results
            if found1 and found2:
                results.income = data1.income
                results.ticker = ticker
                results.strat1 = data1
                results.strat2 = data2
                
                if found3:                 
                    results.strat3 = data3

                return results

            else:
                if found1 == False and found2 == False:
                    results.errorBoo = True
                    results.errorMess = "First two strategies do not exist, please input at least two valid strategies"
                    return results
                elif found1 == False:
                    results.errorBoo = True
                    results.errorMess = "The first strategy does not exist, please input valid strategies"
                    return results

                else:
                    results.errorBoo = True
                    results.errorMess = "The second strategy does not exist, please input valid strategies"
                    return results
        else:
            results.errorBoo = True
            results.errorMess = "Please make sure the start date is earlier than the end date"
            return results

    else:
        results.errorBoo = True
        results.errorMess = "Stock data does not have enough data points for this baseSMA"
        return results