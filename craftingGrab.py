#the purpose of this class is to provide a object 
# that will scrape the web 
# for crafting recipies with cross-refrencing sources
# will return a json
# enabled by default

import bs4
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
import time
class craftingGrabber:
    #dictionary of items 
    crecipie={}
    #simple list of the items that have been visited
    c_visited=[]
    
    
        
    
    
    
    #lets you create a webscraper given specific key terms, and urls. 
    #it can filter out some data but more will have to be filtered manually at a later date
    #xpath is optional but is highly recommended it exists as a backup for the id field check
    #they should all be strings
    #the reason for using a method is 
    #in the hopes of maintaining expandability in case of changes to the official website
    def ffxivScraper(url,id,xpath,className,blockedterms,blockedurls):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        list_of_items = []
        # Get all items on page in a list (their URLs)
        all_questions = driver.find_elements(By.CLASS_NAME, className)
        for question in all_questions:
            list_of_items.append(question.get_attribute("href"))
        print(list_of_items)
        # DB = driver.find_elements(By.CLASS_NAME, className)
        # driver.get
        # for s in range(len(DB)):
        #     DB[s].click()
        
      #  except:
         #   continue
         #   try:
         #       DB = driver.find_element(By.XPATH, xpath)
         #   except:
         #       DB= driver.find_element(By.ID, id)
    
    x = ffxivScraper("https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=1","db-table__txt--detail_link","db-table__txt--detail_link","db-table__txt--detail_link","","" )  
    # print(x)