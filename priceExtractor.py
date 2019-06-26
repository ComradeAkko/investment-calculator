#priceExtractor by Jiro Mizuno

#importing functions
from selenium import webdriver
import os
import webbrowser

#concatenates current URL with ticker
def concatURL(ticker):
    #getting the url for the finance
	base1 = "https://finance.yahoo.com/quote/"
    base2 = "/history?p="
    return base + ticker + base2 + ticker

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
	else:

def getURL(ticker):
    link = concatURL(ticker)
    driver = webdriver.Firefox()
    driver.get(ticker)