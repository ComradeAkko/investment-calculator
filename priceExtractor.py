#priceExtractor by Jiro Mizuno

#importing libraries
import urllib
import os

#concatenates current URL with ticker
def concatURL(ticker):
    #getting the url for the finance
	base = "http://ichart.finance.yahoo.com/table.csv?s="
    return base + ticker

def makeFile(ticker,directory):
    currPath = os.getcwd()
    path = currPath + "/" + directory + "/" + ticker + ".csv"
    return path

def extractHistoricalPrices(ticker, directoryName):
    #get the current path and create a new path
    currPath = os.getcwd()
    directoryPath = currPath + "/" + directoryPath + "/"
    if !(os.path.exists(directoryPath)):
        os.mkdir(directoryPath)
	else
		
    