#priceExtractor by ComradeAkko

#importing functions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import webbrowser
import time

#concatenates current URL with ticker
def concatURL(ticker):
    #getting the url for the finance
	base1 = "https://finance.yahoo.com/quote/"
	base2 = "/history?p="
	return base1 + ticker + base2 + ticker

# def makeFile(ticker,directory):
#     currPath = os.getcwd()
#     path = currPath + "/" + directory + "/" + ticker + ".csv"
#     return path

# def extractHistoricalPrices(ticker, directoryName):
#     #get the current path and create a new path
#     currPath = os.getcwd()
#     directoryPath = currPath + "/" + directoryPath + "/"
#     if !(os.path.exists(directoryPath)):
#         os.mkdir(directoryPath)
# 	else:

def getStockData(ticker):
    #concatenate the url for Yahoo Finance
	link = concatURL(ticker)

    #use the firefox driver

    #set downloading preferences
	profile = webdriver.FirefoxProfile()

	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting",False)
	profile.set_preference("browser.download.dir", os.getcwd())
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

	#set up the Firefox driver and set it so that it waits for elements to appear
	driver = webdriver.Firefox(firefox_profile=profile)
	driver.implicitly_wait(10)

	#open the link
	driver.get(link)

    #clicking the "changing the date path"
	dateButton = driver.find_element_by_xpath("//span[@class='C($c-fuji-blue-1-b) Mstart(8px) Cur(p)']")
	dateButton.click()

    #clicking the "MAX" date
	maxDate = driver.find_element_by_xpath("//span[@data-value='MAX']")
	maxDate.click()

    #clicking the "Done" button
	doneButton = driver.find_element_by_xpath("//button[@class=' Bgc($c-fuji-blue-1-b) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($actionBlueHover):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Miw(80px)! Fl(start)']")
	doneButton.click()

    #clicking the "Apply" button
	applyButton = driver.find_element_by_xpath("//button[@data-reactid='25']")
	applyButton.click()

	#wait for the new url to load
	while(driver.current_url == link):
		time.sleep(0.1)

    #clicking the download button for price data
	downloadButton = driver.find_element_by_xpath("//a[@class='Fl(end) Mt(3px) Cur(p)']")
	downloadButton.click()

	#getting the current URL and replacing it to get dividends data
	currURL = driver.current_url
	newURL = currURL.replace("&interval=1d&filter=history&frequency=1d","&interval=div|split&filter=div&frequency=1d")

	#send random keys to the download button, because it somehow
	#prevents the unknown bug of not loading the next page
	downloadButton.send_keys(Keys.COMMAND)
	
	# get the new url
	driver.get(newURL)

	# clicking the download button for dividend data
	downloadButton = driver.find_element_by_xpath("//a[@class='Fl(end) Mt(3px) Cur(p)']")
	downloadButton.click()

	#wait for the file to be downloaded
	while(os.path.exists(ticker + "(1).csv") == False):
		time.sleep(0.1)

	#rename the files
	os.rename(ticker + ".csv", ticker + "_price.csv")
	os.rename(ticker + "(1).csv", ticker + "_dividend.csv")


	#quitting the driver
	driver.quit()

getStockData("SPY")