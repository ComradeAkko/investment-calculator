#!/usr/bin/env python

#investCalc by ComradeAkko

from priceExtractor import getTreasuryData, getStockData
from datetime import datetime
import sys, csv, operator

data = csv.reader(open('stocks\\SPY\\SPY_dividend.csv'), delimiter=',')
next(data)
sorted(data, key=lambda day: datetime.strptime(day[0], "%Y-%m-%d"),reverse = False)

#need to make sure to delete previous data

#get a treasury bonds returns data
#get some federal tax rates data
#capital gains tax
#comission fees
#sorting data by date