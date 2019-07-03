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

# creates a new bond directory or deletes previous data to make way for new bond data
def newBondDirectory():
	directoryPath = os.getcwd() + "\\bonds"

	#if the directory doesn't exist, make it
	if os.path.exists(directoryPath) == False:
		os.mkdir(directoryPath)

	# if the directory exists, delete the previous data to make way for new data
	else:
		if os.path.isfile(directoryPath + "\\bonds.csv"):
			os.remove(directoryPath + "\\bonds.csv")
		
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
	driver.set_page_load_timeout(15)
	driver.implicitly_wait(5)

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

# gets historical 10-year Treasury Bond yield data
def getTreasuryData():
	# I'm personally using the federal bank of St. Louis's 10-treasury bond yield data 
	url = "https://fred.stlouisfed.org/series/GS10"

	directoryT = newBondDirectory()

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
	os.rename(directoryT + "\\" + "GS10.csv", directoryT + "\\" +  "bonds.csv")

	# sort data
	sortData(directoryT + "\\" +  "bonds.csv")

	# quitting the driver
	driver.quit()

