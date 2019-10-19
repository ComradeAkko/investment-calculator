#!/usr/bin/env python

#priceExtractor by ComradeAkko

#importing functions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os, time, sys, csv, operator

# concatenates current URL with ticker
def concatURL(ticker):
    # getting the url for the finance
	base1 = "https://finance.yahoo.com/quote/"
	base2 = "/history?p="
	return base1 + ticker + base2 + ticker


# creates a new directory with the ticker name and returns the path
def newStockDirectory(ticker):
	directoryPath = os.getcwd() + "\\stocks"

	#if the directory doesn't exist, make it
	if os.path.exists(directoryPath) == False:
		os.mkdir(directoryPath)

	directoryPath += "\\" + ticker

	if os.path.exists(directoryPath) == False:
		os.mkdir(directoryPath)

	# if the directory exists, delete the previous data to make way for new data
	else:
		if os.path.isfile(directoryPath + "\\" + ticker + ".csv"):
			os.remove(directoryPath + "\\" + ticker + ".csv")

		if os.path.isfile(directoryPath + "\\" + ticker + "_price.csv"):
			os.remove(directoryPath + "\\" + ticker + "_price.csv")

		if os.path.isfile(directoryPath + "\\" + ticker + "_dividend.csv"):
			os.remove(directoryPath + "\\" + ticker + "_dividend.csv")
			
		if os.path.isfile(directoryPath + "\\" + ticker + "_split.csv"):
			os.remove(directoryPath + "\\" + ticker + "_split.csv")

	return directoryPath


# creates a new treasury note directory or deletes previous data to make way for new note data
def newTreasuryDirectory():
	directoryPath = os.getcwd() + "\\notes"

	#if the directory doesn't exist, make it
	if os.path.exists(directoryPath) == False:
		os.mkdir(directoryPath)

	# if the directory exists, delete the previous data to make way for new data
	else:
		if os.path.isfile(directoryPath + "\\notes.csv"):
			os.remove(directoryPath + "\\notes.csv")
		
	return directoryPath


# sorts data from the oldest date to the most recent date
def sortData(filePath):
	# open up the file for reading
	data = csv.reader(open(filePath), delimiter=',')
	
	# skip the header
	row = next(data)

	# sort the data
	dataSorted = sorted(data, key=lambda day: datetime.strptime(day[0], "%Y-%m-%d"),reverse = False)

	# writes in the new sorted data
	with open(filePath, newline ='', mode = 'w') as newData:
		dataWriter = csv.writer(newData, delimiter = ',')
		dataWriter.writerow(row)
		for row in dataSorted:
			# if the data is not null write it down
			if row[0] != "null" or row[1] != "null" or row[2] != "null" or row[3] != "null" or row[4] != "null" or row[5] != "null" or row[6] != "null":
				dataWriter.writerow(row)

# sorts data based on alphabet
def sortAlpha(filePath):
	# open up the file for reading
	data = csv.reader(open(filePath), delimiter=',')
	
	# skip the header
	row = next(data)

	# sort the data
	dataSorted = sorted(data, key=lambda alphabet: alphabet[0] ,reverse = False)
	
	# writes in the new sorted data
	with open(filePath, newline ='', mode = 'w') as newData:
		dataWriter = csv.writer(newData, delimiter = ',')
		dataWriter.writerow(row)
		dataWriter.writerows(dataSorted)

# gets historical stock data including prices, dividends, and stock splits
def getStockData(ticker):
    # concatenate the url for Yahoo Finance
	link = concatURL(ticker)

	# create a directory if it doesn't exist and get its path
	directoryP = newStockDirectory(ticker)

    # set downloading preferences
	profile = webdriver.FirefoxProfile()

	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting",False)
	profile.set_preference("browser.download.dir", directoryP)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

	# set up the Firefox driver and set it so that it waits for elements to appear
	driver = webdriver.Firefox(firefox_profile=profile)
	driver.set_page_load_timeout(60)
	driver.implicitly_wait(15)

	# open the link
	driver.get(link)

    # clicking the "changing the date path"
	dateButton = driver.find_element_by_xpath("//span[@class='C($c-fuji-blue-1-b) Mstart(8px) Cur(p)']")
	dateButton.click()

    # clicking the "MAX" date
	maxDate = driver.find_element_by_xpath("//span[@data-value='MAX']")
	maxDate.click()

    # clicking the "Done" button
	doneButton = driver.find_element_by_xpath("//button[@class=' Bgc($c-fuji-blue-1-b) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($actionBlueHover):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Miw(80px)! Fl(start)']")
	doneButton.click()

    # clicking the "Apply" button
	applyButton = driver.find_element_by_xpath("//button[@data-reactid='25']")
	applyButton.click()

	# wait for the new url to load
	while(driver.current_url == link):
		time.sleep(0.1)

    # clicking the download button for price data
	downloadButton = driver.find_element_by_xpath("//a[@class='Fl(end) Mt(3px) Cur(p)']")
	downloadButton.click()

	# getting the current URL and replacing it to get dividends data
	currURL = driver.current_url
	newURL = currURL.replace("&interval=1d&filter=history&frequency=1d","&interval=div|split&filter=div&frequency=1d")

	# getting the new URL and accounting for weird bugs that stall the driver
	finished = 0
	while finished == 0:
		try:
			print("loading new page... (may take a few seconds)")
			driver.get(newURL)
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("page loaded")

	# clicking the download button for dividend data
	downloadButton = driver.find_element_by_xpath("//a[@class='Fl(end) Mt(3px) Cur(p)']")
	downloadButton.click()

	# wait for the file to be downloaded
	while(os.path.isfile(directoryP + "\\" + ticker + "(1).csv") == False):
		time.sleep(0.1)
	
	# getting the current URL and replacing it to get dividends data
	currURL = driver.current_url
	newURL = currURL.replace("&interval=div|split&filter=div&frequency=1d","&interval=div|split&filter=split&frequency=1d")

	# getting the new URL and accounting for weird bugs that stall the driver
	finished = 0
	while finished == 0:
		try:
			print("loading new page... (may take a few seconds)")
			driver.get(newURL)
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("page loaded")

	# clicking the download button for dividend data
	downloadButton = driver.find_element_by_xpath("//a[@class='Fl(end) Mt(3px) Cur(p)']")
	downloadButton.click()

	# wait for the file to be downloaded
	while(os.path.isfile(directoryP + "\\" + ticker + "(2).csv") == False):
		time.sleep(0.1)

	# rename the files
	os.rename(directoryP + "\\" + ticker + ".csv", directoryP + "\\" + ticker + "_price.csv")
	os.rename(directoryP + "\\" + ticker + "(1).csv", directoryP + "\\" + ticker + "_dividend.csv")
	os.rename(directoryP + "\\" + ticker + "(2).csv", directoryP + "\\" + ticker + "_split.csv")

	# sort the data
	sortData(directoryP + "\\" + ticker + "_price.csv")
	sortData(directoryP + "\\" + ticker + "_dividend.csv")
	sortData(directoryP + "\\" + ticker + "_split.csv")


	# quitting the driver
	driver.quit()


# gets historical 10-year Treasury Note yield data
def getTreasuryData():
	# I'm personally using the federal bank of St. Louis's 10-treasury note yield data 
	url = "https://fred.stlouisfed.org/series/GS10"

	directoryT = newTreasuryDirectory()

	# set downloading preferences
	profile = webdriver.FirefoxProfile()

	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting",False)
	profile.set_preference("browser.download.dir", directoryT)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

	# set up the Firefox driver and set it so that it waits for elements to appear
	driver = webdriver.Firefox(firefox_profile=profile)
	driver.set_page_load_timeout(15)
	driver.implicitly_wait(5)

	# open the link
	driver.get(url)

	#click the dowload button
	downloadButton = driver.find_element_by_xpath("//button[@id='download-button']")
	downloadButton.click()

	# getting the data and accounting for weird bugs that occur occasionally
	finished = 0
	while finished == 0:
		try:
			print("extracting data...")
			# click the csv button
			csvButton = driver.find_element_by_xpath("//a[@id='download-data-csv']")
			csvButton.click()
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("data extracted")

	# wait for the file to be downloaded
	while(os.path.isfile(directoryT + "\\" + "GS10.csv") == False):
		time.sleep(0.1)

	# rename the file
	os.rename(directoryT + "\\" + "GS10.csv", directoryT + "\\" +  "notes.csv")

	# sort data
	sortData(directoryT + "\\" +  "notes.csv")

	# quitting the driver
	driver.quit()

def newTickerDirectory():
	directoryPath = os.getcwd() + "\\ticker"

	#if the directory doesn't exist, make it
	if os.path.exists(directoryPath) == False:
		os.mkdir(directoryPath)

	# if the directory exists, delete the previous data to make way for new data
	else:
		if os.path.isfile(directoryPath + "\\nasdaq.csv"):
			os.remove(directoryPath + "\\" + "nasdaq.csv")

		if os.path.isfile(directoryPath + "\\nyse.csv"):
			os.remove(directoryPath + "\\" + "nyse.csv")

		if os.path.isfile(directoryPath + "\\amex.csv"):
			os.remove(directoryPath + "\\" + "amex.csv")

		if os.path.isfile(directoryPath + "\\etf.csv"):
			os.remove(directoryPath + "\\" + "etf.csv")

		if os.path.isfile(directoryPath + "\\ETFList.csv"):
			os.remove(directoryPath + "\\" + "ETFList.csv")
			
		if os.path.isfile(directoryPath + "\\companylist.csv"):
			os.remove(directoryPath + "\\companylist.csv")

		if os.path.isfile(directoryPath + "\\companylist(1).csv"):
			os.remove(directoryPath + "\\companylist(1).csv")

		if os.path.isfile(directoryPath + "\\companylist(2).csv"):
			os.remove(directoryPath + "\\companylist(2).csv")
		
	return directoryPath


# gets the list of tickers on the NYSE markets 
def getTickerList():

	directoryTick = newTickerDirectory()

	# set downloading preferences
	profile = webdriver.FirefoxProfile()

	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting",False)
	profile.set_preference("browser.download.dir", directoryTick)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/text, Application/ms-excel; charset=utf-8")

	# set up the Firefox driver and set it so that it waits for elements to appear
	driver = webdriver.Firefox(firefox_profile=profile)
	driver.set_page_load_timeout(15)
	driver.implicitly_wait(5)

	# get the url for companies
	url = "https://www.nasdaq.com/screening/company-list.aspx"

	# getting the URL and accounting for weird bugs that stall the driver
	finished = 0
	while finished == 0:
		try:
			print("loading new page... (may take a few seconds)")
			driver.get(url)
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("page loaded")

	#click the cookie button
	finished = 0
	while finished == 0:
		try:
			print("clicking the cookie button...")
			# click the csv button
			cookieButton = driver.find_element_by_xpath("//a[@id='cookieConsentOK']")
			cookieButton.click()
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("cookie button clicked")

	# getting the data and accounting for weird bugs that occur occasionally
	finished = 0
	while finished == 0:
		try:
			print("extracting NASDAQ data...")
			# click the csv button
			nasdaqButton = driver.find_element_by_xpath("//a[@href='https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download']")
			nasdaqButton.click()
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("data extracted")

	# getting the data and accounting for weird bugs that occur occasionally
	finished = 0
	while finished == 0:
		try:
			print("extracting NYSE data...")
			# click the csv button
			nyseButton = driver.find_element_by_xpath("//a[@href='https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download']")
			nyseButton.click()
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("data extracted")

	# getting the data and accounting for weird bugs that occur occasionally
	finished = 0
	while finished == 0:
		try:
			print("extracting AMEX data...")
			# click the csv button
			amexButton = driver.find_element_by_xpath("//a[@href='https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download']")
			amexButton.click()
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("data extracted")

	newURL = "https://www.nasdaq.com/etfs/list"

	# getting the new URL and accounting for weird bugs that stall the driver
	finished = 0
	while finished == 0:
		try:
			print("loading new page... (may take a few seconds)")
			driver.get(newURL)
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("page loaded")

	# getting the data and accounting for weird bugs that occur occasionally
	finished = 0
	while finished == 0:
		try:
			print("extracting etf data...")
			# click the csv button
			etfButton = driver.find_element_by_xpath("//a[@href='https://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes']")
			etfButton.click()
			finished = 1
		except:
			print("trying again...")
			time.sleep(5)
	print("data extracted")

	# rename the files
	os.rename(directoryTick + "\\companylist.csv", directoryTick + "\\nasdaq.csv")
	os.rename(directoryTick + "\\companylist(1).csv", directoryTick + "\\nyse.csv")
	os.rename(directoryTick + "\\companylist(2).csv", directoryTick + "\\amex.csv")
	os.rename(directoryTick + "\\ETFList.csv", directoryTick + "\\etf.csv")

	# sort the data
	sortAlpha(directoryTick + "\\" + "nasdaq.csv")
	sortAlpha(directoryTick + "\\" + "nyse.csv")
	sortAlpha(directoryTick + "\\" + "amex.csv")
	sortAlpha(directoryTick + "\\" + "etf.csv")

	# quitting the driver
	driver.quit()