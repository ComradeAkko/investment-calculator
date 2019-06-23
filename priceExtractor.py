#priceExtractor by Jiro Mizuno

#importing libraries
import urllib
import os

#getting the url for the finance
base = "http://ichart.finance.yahoo.com/table.csv?s="

#concatenates current URL with ticker
def concatURL(ticker):
    return base + ticker

def makeFile(ticker,directory):
    currPath = os.getcwd()
    directoryPath = currPath + "/" + directoryPath + "/"
    return 

def extractHistoricalPrices(ticker, directoryName):
    #get the current path and create a new path
    currPath = os.getcwd()
    directoryPath = currPath + "/" + directoryPath + "/"
    if !(os.path.exists(directoryPath)):
        os.mkdir(directoryPath)
    