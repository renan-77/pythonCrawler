#Importing the webdriver from selenium.
from selenium import webdriver

#Importing the chrome option to set it up.
from selenium.webdriver.chrome.options import Options

#Importing time to use the sleep function.
import time

#Setting the options for chrome.
options = Options()
options.add_argument("--incognito")
options.add_argument("--window-size=1440x900")

#Setting a driver variable for the chrome webdriver.
driver = webdriver.Chrome(options=options, executable_path='/Users/renan/Dropbox/Working/python/currencyChecker/chromedriver')

#Setting url for the crawler
url = "https://www.xe.com/"

#Specifying the url to be accessed using the driver function.
driver.get(url)

#Sleep of two seconds before returning the access.
time.sleep(2)

#Declaring a variable to find an element on the website through xpath 
okButton = driver.find_element_by_xpath("//button[@class='privacy-basic-button privacy-basic-button-submit'][@type='submit']")

print(okButton.text)

#Clicks the ok button for confirming cookies.
okButton.click()

#Creating array with the text found in the page (currencies).
eurCurrencies = [driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[1]/a').text, 
driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[2]/a').text,
driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[3]/a').text, 
driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[4]/a').text] 

#Printing the currencies with the array values..
print('1 EURO = USD: ' ,eurCurrencies[1],'$ GPB: ' , eurCurrencies[2],'£ CAD: ' , eurCurrencies[3] ,'$.')
