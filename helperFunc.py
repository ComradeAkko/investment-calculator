# helperFunc.py by ComradeAkko

# returns a boolean based on whether the csv file contains data

import csv, operator, math, os
from datetime import datetime

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
            divsplit = eval(row[1])
            file.close()
            return divsplit

# returns the 10 year treasury note yield for stated month
def getNoteYield(date, datapath):
    file = open(datapath)
    data = csv.reader(file)

    #skip the header
    next(data)
    
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
    return (eb/bb)**(1/n) - 1

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
    return (d1.year - d2.year) * 12 + d1.month - d2.month

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

    # listify the data
    data = list(data)

    # figure out which index holds the current date
    for i in range(1, len(data)):
        if date == data[i][0]:
            index = i
            break

    # isolate the relevant rows
    movingAverageRows = data[index-period:index]

    # calculate the current sum
    sum = 0
    for row in movingAverageRows:
        sum += float(row[4])
    
    # get the average
    SMA = sum/period

    file.close()
    
    return SMA
