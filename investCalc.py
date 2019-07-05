#!/usr/bin/env python

#investCalc by ComradeAkko

from priceExtractor import getTreasuryData, getStockData
from datetime import datetime
import csv, operator

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

# calculates the current moving average based on the period
# and the current date
def movingAverage(period):


def investCalc(ticker, income, investFrac, initial, strat, monthly):



# calculate 200 day moving average
# calculate 50 day moving average
# calculate buying and selling


# disclaimer about how the current model doesn't use historical data on tax rates
# disclaimer about how the current model doesn't use historical capital gains tax rates 