#priceExtractor by Jiro Mizuno

#importing libraries
import urllib
import os

#getting the url for the finance
base = "http://ichart.finance.yahoo.com/table.csv?s="

#concatenates current URL with ticker
def concatURL(ticker):
    return base + ticker

#get the current path and create a new path
currPath = os.getcwd()
outputPath = 