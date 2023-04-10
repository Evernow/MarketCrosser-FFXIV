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
        #list of the hyperlinks of the items that were unsuccesfully visited
        self.errvisited=[]
        
     

    
        
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
        driver = webdriver.Firefox()
        driver.get(url)
        ingredientlst={}
        errorchk=True
        
        linklist=self.ffxivItemHyperlinkScraper(url,className)
        for vars in linklist:
            #makes the current scope the page of the new element
            #also adds a link to a page if its unable to connect where it will attempt again in 1 hr
            try:
                driver.get(vars)
                errorchk=True
            except:
                print("there is some issue with connecting to one or more of the items we will retry those missing in 1hr")
                self.errvisited.append(vars)
                errorchk=False
                
        
            if(errorchk):
                #name of the crafted item
                namex=driver.find_element(By.CLASS_NAME,"db-view__item__text__name")
                name=namex.text
                
                #name of the job required to craft
                jobx=driver.find_element(By.CLASS_NAME,"db-view__item__text__job_name")
                job=jobx.text
                
                #catagory of the item 
                categoryx=driver.find_element(By.CLASS_NAME,"db-view__recipe__text__category")
                category=categoryx.text
                
                #sorts through strings to find different stats from crafting that can be used for sorting
                stuffx=driver.find_element(By.CLASS_NAME,"db-view__recipe__craftdata")
                stuff=stuffx.text
                
                #length is one extra to account for the space
                TClocb=stuff.find("Total Crafted")+14
                TClocc=stuff.find("Difficulty")
                Dlocb=stuff.find("Difficulty")+11
                Dlocc=stuff.find("Durability")
                #total amount of the item crafted from a single craft
                totalCrafted=stuff[TClocb:TClocc]
                #items crafting difficulty
                diff=stuff[Dlocb:Dlocc]
                #turns them into ints
                diff=int(diff)
                totalCrafted=int(totalCrafted)
                
                #returns the level required to craft
                levelx=driver.find_element(By.CLASS_NAME,"db-view__item__text__level__inner")
                level=levelx.text
                level=level[3:]
                
                #dict of ingredients and the amount of them required
                ingredients={}
                #name of ingredients and amount of ingredients in a list
                ingredients_name=""
                ingredients_amt=0
                #note this containes both the name and the number of items we need to parse thru these and assign them
                ingredientsx=driver.find_elements(By.CLASS_NAME,"db-view__data__reward__item__name")
                #filter and assigns peices of ingredientsx
                
                for ing in ingredientsx:
                    ingredients_amt=((ing.find_element(By.CLASS_NAME, "db-view__item_num")).text)
                    ingredients_name=((ing.find_element(By.CLASS_NAME, "db_popup")).text)
                    ingredients[ingredients_name]=ingredients_amt
                #ingredient creation
                ingredientlst[name]={"Job":job, "Category":category,"Level":level, "Difficulty":diff, "Amount from craft":totalCrafted,"Ingredients":ingredients}
       
        #code for fixing errors in retrieval
        while(self.errvisited!=[]):
            for vars in list(self.errvisited):
                #makes the current scope the page of the new element
                #also adds a link to a page if its unable to connect where it will attempt again in 1 hr
                
                try:
                    driver.get(vars)
                    errorchk=True
                    self.errvisited.remove(vars)
                    
                except:
                    print("there is some issue with connecting to one or more of the items we will retry those missing in 1hr")
                    errorchk=False
                    
            
                if(errorchk):
                    #name of the crafted item
                    namex=driver.find_element(By.CLASS_NAME,"db-view__item__text__name")
                    name=namex.text
                    
                    #name of the job required to craft
                    jobx=driver.find_element(By.CLASS_NAME,"db-view__item__text__job_name")
                    job=jobx.text
                    
                    #catagory of the item 
                    categoryx=driver.find_element(By.CLASS_NAME,"db-view__recipe__text__category")
                    category=categoryx.text
                    
                    #sorts through strings to find different stats from crafting that can be used for sorting
                    stuffx=driver.find_element(By.CLASS_NAME,"db-view__recipe__craftdata")
                    stuff=stuffx.text
                    
                    #length is one extra to account for the space
                    TClocb=stuff.find("Total Crafted")+14
                    TClocc=stuff.find("Difficulty")
                    Dlocb=stuff.find("Difficulty")+11
                    Dlocc=stuff.find("Durability")
                    #total amount of the item crafted from a single craft
                    totalCrafted=stuff[TClocb:TClocc]
                    #items crafting difficulty
                    diff=stuff[Dlocb:Dlocc]
                    #turns them into ints
                    diff=int(diff)
                    totalCrafted=int(totalCrafted)
                    
                    #returns the level required to craft
                    levelx=driver.find_element(By.CLASS_NAME,"db-view__item__text__level__inner")
                    level=levelx.text
                    level=level[3:]
                    
                    #dict of ingredients and the amount of them required
                    ingredients={}
                    #name of ingredients and amount of ingredients in a list
                    ingredients_name=""
                    ingredients_amt=0
                    #note this containes both the name and the number of items we need to parse thru these and assign them
                    ingredientsx=driver.find_elements(By.CLASS_NAME,"db-view__data__reward__item__name")
                    #filter and assigns peices of ingredientsx
                    
                    for ing in ingredientsx:
                        ingredients_amt=((ing.find_element(By.CLASS_NAME, "db-view__item_num")).text)
                        ingredients_name=((ing.find_element(By.CLASS_NAME, "db_popup")).text)
                        ingredients[ingredients_name]=ingredients_amt
                    #ingredient creation
                    ingredientlst[name]={"Job":job, "Category":category,"Level":level, "Difficulty":diff, "Amount from craft":totalCrafted,"Ingredients":ingredients}
            print(ingredientlst)
            
        
        
scraper=craftingGrabber() 
scraper.ffxivScraper("https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=205","db-table__txt--detail_link")