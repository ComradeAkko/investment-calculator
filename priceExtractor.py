#priceExtractor by ComradeAkko

#importing functions
from selenium import webdriver
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

def getPrices(ticker):
    #concatenate the url for Yahoo Finance
	link = concatURL(ticker)

    #use the firefox driver

    #set downloading preferences
	profile = webdriver.FirefoxProfile()

	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting",False)
	profile.set_preference("browser.download.dir", os.getcwd())
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

	#set up the Firefox driver
	driver = webdriver.Firefox(firefox_profile=profile)
	driver.get(link)

    #clicking the "changing the date path"
	dateButton = driver.find_element_by_xpath("//span[@class='C($c-fuji-blue-1-b) Mstart(8px) Cur(p)']")
	dateButton.click()

	time.sleep(0.25)

    #clicking the "MAX" date
	maxDate = driver.find_element_by_xpath("//span[@data-value='MAX']")
	maxDate.click()

	time.sleep(0.25)

    #clicking the "Done" button
	doneButton = driver.find_element_by_xpath("//button[@class=' Bgc($c-fuji-blue-1-b) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($actionBlueHover):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Miw(80px)! Fl(start)']")
	doneButton.click()

	time.sleep(0.25)

    #clicking the "Apply" button
	applyButton = driver.find_element_by_xpath("//button[@data-reactid='25']")
	applyButton.click()

	time.sleep(0.25)

    #clicking the download button
	downloadButton = driver.find_element_by_xpath("//a[@class='Fl(end) Mt(3px) Cur(p)']")
	downloadButton.click()

	#quitting the driver
	driver.quit()


getPrices("MSFT")