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

#Type of currency to display.
whichCurrency = "GBP"

#Creating global time now variable.
now = datetime.datetime.now()

#Function that creates mongodb connection and starts the software.
def databaseConnection(ip,port):
    #Try and catch block to check connection.
    try:
        conn = MongoClient(ip,port)
        print("Successfully Connected to database")
    except:
        print("Database connection error, please check data")
    db = conn.currencyChecker
    collection = db.currencies

    #Evoking the insert on database method.
    databaseInsert(collection)

#Function to insert the data onto the database.
def databaseInsert(db_collection):
    #Assigning a dataset variable to the returned array from seleniumDriver function.
    dataset = seleniumDriver('https://www.xe.com/', '/Users/renan/Dropbox/Working/python/currencyChecker/chromedriver')

    #Inserting the currencies to the database.
    db_collection.insert_one({"currency" : "USD", "currentValue" : dataset[0] , "when" : str(now)})
    db_collection.insert_one({"currency" : "GBP", "currentValue" : dataset[1] , "when" : str(now)})
    db_collection.insert_one({"currency" : "CAD", "currentValue" : dataset[2] , "when" : str(now)})

    #Evoking databaseFind method with the collection as argument.
    databaseFind(db_collection)

def seleniumDriver(url, driverPath):
    #Setting the options for chrome.
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1440x900")

    #Setting a driver variable for the chrome webdriver.
    driver = webdriver.Chrome(options=options, executable_path=driverPath)

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

    #Creating array with the text found in the page (currencies).
    eurCurrencies = [driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[1]/a').text, 
    driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[2]/a').text,
    driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[3]/a').text, 
    driver.find_element_by_xpath('//*[@id="ratesTable"]/div/section/table/tbody/tr[2]/td[4]/a').text] 

    #Printing the currencies with the array values..
    print('CURRENT CURRENCY: 1 EURO = USD: ' ,eurCurrencies[0],'$ GPB: ' , eurCurrencies[1],'£ CAD: ' , eurCurrencies[2] ,'$.', 'Query time:', str(now))

    #Returning the euCurrencies array.
    return eurCurrencies

#Function to retrive the data from the database and add to a file.
def databaseFind(db_collection):
    #Creating range of find to print the documents in the range.
    cur = db_collection.find({"currency": whichCurrency}, {"_id" : 0, "currency" : 1 ,"currentValue" : 1, "when" : 1})

    #Checking the count of existing registers on currency for naming files.
    currencyRegisterCount = "{0}{1}".format(whichCurrency, db_collection.count_documents({"currency" : whichCurrency}))

    #Creating text file to output.
    if(db_collection.count_documents({"currency" : whichCurrency}) != 0):
        File_object = open("currencies%s.txt" % currencyRegisterCount,"w+")
    else:
        print("Data check fail.")

    #For loop to get every document in the cursor.
    for currentCurrency in cur:        
        #Outputing the result to the created text file.
        File_object.write("%s\n" % currentCurrency)

#Calling databaseConnection function.
databaseConnection('localhost',27017)