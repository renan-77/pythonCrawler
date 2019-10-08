#Importing the webdriver from selenium.
from selenium import webdriver
#Importing the Client for mongodb from pymongo.
from pymongo import MongoClient
#Importing date and time to get current. 
import datetime
#Importing the chrome option to set it up.
from selenium.webdriver.chrome.options import Options
#Importing time to use the sleep function.
import time

#Creating mongodb connection.
try:
    conn = MongoClient('localhost',27017)
    print("Successfully Connected to database")
except:
    print("Database connection error, please check data")
db = conn.currencyChecker
collection = db.currencies

#Setting the options for chrome.
options = Options()
options.add_argument("--incognito")
options.add_argument("--window-size=1440x900")

#Setting a driver variable for the chrome webdriver.
driver = webdriver.Chrome(options=options, executable_path='/Users/renan/Dropbox/Working/python/currencyChecker/chromedriver')

#Setting url for the crawler.
url = "https://www.xe.com/"

#Specifying the url to be accessed using the driver function.
driver.get(url)

#Sleep of two seconds before returning the access.
time.sleep(2)

#Declaring a variable to find an element on the website through xpath. 
okButton = driver.find_element_by_xpath("//button[@class='privacy-basic-button privacy-basic-button-submit'][@type='submit']")

#Confirmation that the button was found printing it's text.
print(okButton.text)

#Clicks the ok button for confirming cookies.
okButton.click()

#Getting current date and time and assigning to "now" variable.
now = datetime.datetime.now()

#Creating array with the text found in the page (currencies).
eurCurrencies = [driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[1]/a').text, 
driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[2]/a').text,
driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[3]/a').text, 
driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[4]/a').text] 

#Printing the currencies with the array values..
print('CURRENT CURRENCY: 1 EURO = USD: ' ,eurCurrencies[0],'$ GPB: ' , eurCurrencies[1],'£ CAD: ' , eurCurrencies[2] ,'$.', 'Query time:', str(now))

#Inserting the currencies to the database.
collection.insert_one({"currency" : "USD", "currentValue" : eurCurrencies[0] , "when" : str(now)})
collection.insert_one({"currency" : "GPB", "currentValue" : eurCurrencies[1] , "when" : str(now)})
collection.insert_one({"currency" : "CAD", "currentValue" : eurCurrencies[2] , "when" : str(now)})

#Type of currency to display.
whichCurrency = "USD"

#Creating range of find to print the documents in the range.
cur = collection.find({"currency": whichCurrency}, {"_id" : 0, "currency" : 1 ,"currentValue" : 1, "when" : 1})

#Checking the count of existing registers on currency for naming files.
currencyRegisterCount = "{0}{1}".format(whichCurrency, collection.count_documents({"currency" : whichCurrency}))

#Creating text file to output.
if(collection.count_documents({"currency" : whichCurrency}) != 0):
    File_object = open("currencies%s.txt" % currencyRegisterCount,"w+")
else:
    print("Data check fail.")

#For loop to get every document in the cursor.
for currentCurrency in cur:
    #print(currentCurrency)
    
    #Outputing the result to the created text file.
    File_object.write("%s\n" % currentCurrency)

#Closing browser after operation is finished.
driver.quit()