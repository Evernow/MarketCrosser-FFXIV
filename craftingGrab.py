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
    global links, crecipie, c_visited
    #dictionary of items 
    crecipie={}
    #simple list of the items that have been visited
    c_visited=[]
    #list of the hyperlinks of all the items
    links =[]
    #returns the hyperlink of items given the 

    
        
    def materials():
        exit
    
    
    #lets you create a webscraper given specific key terms, and urls. 
    #it can filter out some data but more will have to be filtered manually at a later date
    #xpath is optional but is highly recommended it exists as a backup for the id field check
    #they should all be strings
    #the reason for using a method is 
    #in the hopes of maintaining expandability in case of changes to the official website
    def ffxivScraper(url,id,xpath,className,blockedterms,blockedurls):
        nextprev,materials,crystals,level,job="",[],[],1,None 
        
        driver = webdriver.Firefox()
        driver.get(url)
        x=True
        while(x==True):
        
        #  try:
            DB = driver.find_elements(By.CLASS_NAME, className)
            driver.get
        #  this rotates thru and assigns the href value to all the functions(hyperlinks)
            for s in range(len(DB)):
                links.append(DB[s].get_attribute("href"))
                #clicks the next one
            try:
                tonext=driver.find_element(By.CLASS_NAME, "next")
                tonext.click()
            except:
                x=False
        
      #  except:
         #   continue
         #   try:
         #       DB = driver.find_element(By.XPATH, xpath)
         #   except:
         #       DB= driver.find_element(By.ID, id)
         
         
         
    ffxivScraper("https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=205","db-table__txt--detail_link","db-table__txt--detail_link","db-table__txt--detail_link","","" )