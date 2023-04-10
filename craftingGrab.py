#the purpose of this class is to provide a object 
# that will scrape the web 
# for crafting recipies with cross-refrencing sources
# will return a json
# enabled by default

import bs4
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions
import json
import time
class craftingGrabber:
    def __init__(self):
#standard vars
    #dictionary of items 
        self.crecipie={}
        #simple list of the hyperlinks of items to visit
        self.links =[]
    #sanity checking variables
        #list of the hyperlinks of all the items that have been visited successfully
        self.s_visited=[]
        #list of the hyperlinks of the items that were unsuccesfully visited
        self.e_visited=[]
     

    
        
    def materials():
        exit
    
    
    #lets you create a webscraper given specific key terms, and urls. 
    #it can filter out some data but more will have to be filtered manually at a later date
    #xpath is optional but is highly recommended it exists as a backup for the id field check
    #they should all be strings
    #the reason for using a method is 
    #in the hopes of maintaining expandability in case of changes to the official website
    def ffxivItemHyperlinkScraper(self,url,className):
        #initialconnect is used to count the while loop times it took to connect
        initialconnect=True
        driver = webdriver.Firefox()
        driver.get(url)
        
        #encased will redo the whole initial connection if the website is down after 10 seconds
        while(initialconnect):
            try:
                tonext=driver.find_element(By.CLASS_NAME, "next")
                initialconnect=False
            except:
                print("something went wrong when connecting to the ffxiv server trying again in 10 mins. . .")
                time.sleep(600)
    #the next element is the object that identifies the next page of the db on the web
        tonext=driver.find_element(By.CLASS_NAME, "next")
    #the last page to scan and where to stop
        last=driver.find_element(By.CLASS_NAME, "next_all").find_element(By.TAG_NAME, "a").get_attribute("href")
    #the next page to scan
        nextprev=tonext.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(last, "/n")
        traverse=True
        
        #rotates through the entire library of craftable items 
        while(traverse):
            #Identifies the items and the next page
            DB = driver.find_elements(By.CLASS_NAME, className)
        #  this rotates thru and assigns the href value to all the functions(hyperlinks)
            for s in range(len(DB)):
                self.links.append(DB[s].get_attribute("href"))
            #clicks the next page if there is one
            if(nextprev!=last):
                tonext=driver.find_element(By.CLASS_NAME, "next")
                nextprev=tonext.find_element(By.TAG_NAME, "a").get_attribute("href")
                tonext.click()
                tonext=driver.find_element(By.CLASS_NAME, "next")
            else:
                traverse=False
                break
        return(self.links)
    
    def ffxivScraper(self,url,className):
        self.ffxivItemHyperlinkScraper(url,className)
        
scraper=craftingGrabber() 
scraper.ffxivScraper("https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=205","db-table__txt--detail_link")