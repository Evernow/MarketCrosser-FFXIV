# the purpose of this class is to provide a object 
# that will naturally scrape the officially ffxiv website  
# to create a structured json based dictionary
# FIREFOX IS A MANDATORY DEPENDENCY!!!! 
# Use of other webdrivers can potentially cause instabilities or undefined behavior. Do so at your own risk
# Tested for use under Linux and Windows, untested on MACOS but should work
# This was not programmed with concurrency/multithreading in mind and will thus run into issues if you attempt to do such

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import StaleElementReferenceException
import multipledispatch
import json
import time
import requests

class ffxiv_grabber:
    def __init__(self, Gather_Url, Craft_Url):
#standard vars
        self.gather_url=Gather_Url
        self.craft_url=Craft_Url
        #should be static dont change this
        self.GARLANDAPI="https://garlandtools.org/api/get.php"
        self.GARLANDSRC="https://garlandtools.org/db/doc/core/en/3/data.json"
        self.ITEMLST="https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/staging/libs/data/src/lib/json/items.json"
      #dictionary of items 
        self.crecipie={}
        #simple list of the hyperlinks of items to visit
        self.links =[]
    #sanity checking variables
        #list of the hyperlinks of the items that were unsuccesfully visited
        self.errvisited=[]
    #options to use when creating a new instance of a webdriver
        #this should stabilize behaviors across operating systems
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.set_preference("general.useragent.override", "userAgent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0")
        
    def updateIDDB(self):
      request=requests.get(self.ITEMLST)
      request=request.json()
      with open("itemid.json", "w+") as outfile:
        json.dump(request, outfile, indent =6)
    
    
    #lets you create a ffxiv webscraper given specific db location, and urls. 
    #they should all be strings
    #the reason for using a method is 
    #in the hopes of maintaining expandability in case of changes to the official website
    def ffxivItemHyperlinkScraper(self,url,className):
        #initialconnect is used to count the while loop times it took to connect
        initialconnect=True
        
        driver = webdriver.Firefox(options=self.options)
        driver.get(url)
        counter=0
        
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
        traverse=True
        
        #rotates through the entire library of craftable items 
            
        while(traverse):
            #Identifies the items and the next page
            DB = driver.find_elements(By.CLASS_NAME, className)
            counter=counter+1
            print(counter, "DB pages scanned", end='\r')
        #  this rotates thru and assigns the href value to all the functions(hyperlinks)
            for s in range(len(DB)):
              try:
                self.links.append(DB[s].get_attribute("href"))
              except NoSuchAttributeException:
                print("Note: one or more items did not contain a hyperlink \n and will thus be omitted")
                
            #clicks the next page if there is one
            if(nextprev!=last):
                tonext=driver.find_element(By.CLASS_NAME, "next")
                nextprev=tonext.find_element(By.TAG_NAME, "a").get_attribute("href")
                tonext.click()
                tonext=driver.find_element(By.CLASS_NAME, "next")
            else:
                traverse=False
                break
        print("\n")
        return(self.links)
    
    def ffxivCraftScraper(self,className):
      url=self.craft_url
      driver = webdriver.Firefox(options=self.options)
      driver.get(url)
      ingredientlst={}
      errorchk=True
      countse=0
      counterr=0
      linklist=self.ffxivItemHyperlinkScraper(url,className)
      for vars in linklist:
          #makes the current scope the page of the new element
          #also adds a link to a page if its unable to connect where it will attempt again in 1 hr
          try:
              driver.get(vars)
              errorchk=True
              countse=countse+1
          except:
              print("there is some issue with connecting to one or more of the items we will retry those missing in 1hr")
              print("the url that failed is:", vars, "\n")
              self.errvisited.append(vars)
              errorchk=False
              counterr=counterr+1
          print(countse," items have been scanned out of ",len(linklist)," with ", counterr, " errors ",  end='\r')


          if(errorchk):
              try:
                namex=driver.find_element(By.CLASS_NAME,"db-view__item__text__name")
                name=namex.text
              except NoSuchElementException:
                name="NULL"
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
                continue
              
              #name of the job required to craft
              try:
                jobx=driver.find_element(By.CLASS_NAME,"db-view__item__text__job_name")
                job=[jobx.text]
              except NoSuchElementException:
                job="NULL"
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
                continue

              #catagory of the item
              try: 
                categoryx=driver.find_element(By.CLASS_NAME,"db-view__recipe__text__category")
                category=categoryx.text
              except NoSuchElementException:
                category="NULL"
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
                continue

              #sorts through strings to find different stats from crafting that can be used for sorting
              try:
                stuffx=driver.find_element(By.CLASS_NAME,"db-view__recipe__craftdata")
                stuff=stuffx.text
              except NoSuchElementException:
                stuff="NULL"
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
                continue
                

              #length is one extra to account for the space
              try:
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
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
                continue
                
              #returns the level required to craft
              try:
                levelx=driver.find_element(By.CLASS_NAME,"db-view__item__text__level__inner")
                level=levelx.text
                level=level[3:]
              except NoSuchElementException:
                level="NULL"
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
              
              #dict of ingredients and the amount of them required
              ingredients={}
              #name of ingredients and amount of ingredients in a list
              ingredients_name=""
              ingredients_amt=0
              #note this containes both the name and the number of items we need to parse thru these and assign them
              try:
                ingredientsx=driver.find_elements(By.CLASS_NAME,"db-view__data__reward__item__name")
                #filter and assigns peices of ingredientsx
                
                for ing in ingredientsx:
                    ingredients_amt=((ing.find_element(By.CLASS_NAME, "db-view__item_num")).text)
                    ingredients_name=((ing.find_element(By.CLASS_NAME, "db_popup")).text)
                    ingredients[ingredients_name]=ingredients_amt
                    
                #ingredient creation as well as duplication prevention
                if name in ingredientlst:
                  ingredientlst[name]["Job"]=ingredientlst[name]["Job"] +job
                   #the other crafters recipie will be added as another list 
                  ingredientlst[name]["Ingredients"]=ingredientlst[name]["Ingredients"] + [ingredients]


                else:
                  ingredientlst[name]={"Job":job, "Category":category,"Level":level, "Difficulty":diff, "Amount from craft":totalCrafted,"Ingredients":[ingredients]}
              except NoSuchElementException:
                ingredientlst[name]="NULL"
              except StaleElementReferenceException:
                self.errvisited.append(vars)
                errorchk=False
                counterr=counterr+1
#code for fixing errors in retrieval
      dummy=self.errvisited
      countse=0
      counterr=0
      while(list(self.errvisited)!=[]):
          #3600 seconds is 1 hr
          time.sleep(3600)
          count=1
          while(list(self.errvisited)!=[] and len(dummy)<=count):
              #dummy serves to prevent weird & undocumented python behaviors 
              #with deleting values from an array currently being traversed 
              dummy=self.errvisited
              for vars in list(dummy):
                  count=count+1
                  #makes the current scope the page of the new element
                  #also adds a link to a page if its unable to connect where it will attempt again in 1 hr
                  
                  try:
                      driver.get(vars)
                      errorchk=True
                      self.errvisited.remove(vars)
                      dummy=self.errvisited
                      countse=countse+1
                      
                      
                  except:
                      print("there is some issue with connecting to one or more of the items we will retry those missing in 1hr")
                      print("the url that failed is:", vars)
                      errorchk=False
                      counterr=counterr+1
                      
                  print(countse," erronious items have been scanned out of ",len(dummy)," with ", counterr, " errors ",  end='\r')
              
                  if(errorchk):
                    try:
                      namex=driver.find_element(By.CLASS_NAME,"db-view__item__text__name")
                      name=namex.text
                    except NoSuchElementException:
                      name="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    
                    #name of the job required to craft
                    try:
                      jobx=driver.find_element(By.CLASS_NAME,"db-view__item__text__job_name")
                      job=[jobx.text]
                    except NoSuchElementException:
                      job="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue

                    #catagory of the item
                    try: 
                      categoryx=driver.find_element(By.CLASS_NAME,"db-view__recipe__text__category")
                      category=categoryx.text
                    except NoSuchElementException:
                      category="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue

                    #sorts through strings to find different stats from crafting that can be used for sorting
                    try:
                      stuffx=driver.find_element(By.CLASS_NAME,"db-view__recipe__craftdata")
                      stuff=stuffx.text
                    except NoSuchElementException:
                      stuff="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue

                    #length is one extra to account for the space
                    try:
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
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                      
                    #returns the level required to craft
                    try:
                      levelx=driver.find_element(By.CLASS_NAME,"db-view__item__text__level__inner")
                      level=levelx.text
                      level=level[3:]
                    except NoSuchElementException:
                      level="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                      
                    #dict of ingredients and the amount of them required
                    ingredients={}
                    #name of ingredients and amount of ingredients in a list
                    ingredients_name=""
                    ingredients_amt=0
                    #note this containes both the name and the number of items, we need to parse thru these and assign them
                    try:
                      ingredientsx=driver.find_elements(By.CLASS_NAME,"db-view__data__reward__item__name")
                      
                        #filter and assigns peices of ingredientsx to ingredients
                      for ing in ingredientsx:
                        ingredients_amt=((ing.find_element(By.CLASS_NAME, "db-view__item_num")).text)
                        ingredients_name=((ing.find_element(By.CLASS_NAME, "db_popup")).text)
                        ingredients[ingredients_name]=ingredients_amt
                    
                        #ingredient creation as well as duplication prevention
                      if name in ingredientlst:
                        #in the case of duplicate items the other crafter will be added to the other
                       ingredientlst[name]["Job"]=ingredientlst[name]["Job"] + job
                        #the other crafters recipie will be added as another list 
                       ingredientlst[name]["Ingredients"]=ingredientlst[name]["Ingredients"] + [ingredients]

                      else:
                        ingredientlst[name]={"Job":job, "Category":category,"Level":level, "Difficulty":diff, "Amount from craft":totalCrafted,"Ingredients":[ingredients]}
                    except NoSuchElementException:
                      ingredientlst[name]="NULL"  
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    
                      
    #saves the official file 
      with open("Ffxivcrafting.json", "w+") as outfile:
        json.dump(ingredientlst, outfile, indent = 6)    
    
    #used in conjunction with garland api for cross refrencing data for sanity
    def ffxivGatherScraper(self,className):
      #gets the previously set gathering url
      url=self.gather_url  
      driver = webdriver.Firefox(options=self.options)
      driver.get(url)
      
      errorchk=True
      countse=0
      gatherlst={}
      counterr=0
      #calls the function to scrape the url of all the items listed in the official DB
      linklist=self.ffxivItemHyperlinkScraper(url,className)
      #wipes the errvisited list
      self.errvisited=[]
      for vars in linklist:
        try:
            driver.get(vars)
            errorchk=True
            countse=countse+1
        except:
            print("there is some issue with connecting to one or more of the items we will retry those missing in 1hr")
            print("the url that failed is:", vars, "\n")
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
        print(countse," items have been scanned out of ",len(linklist)," with ", counterr, " errors ",  end='\r')
        #name of the job required to craft
        if errorchk:
          try:
            jobx=driver.find_element(By.CLASS_NAME,"db-view__item__text__job_name")
            job=[jobx.text]
          except NoSuchElementException:
            job="NULL"
          except StaleElementReferenceException:
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
            continue
          #get the name of the item to gather
          try:
            namex=driver.find_element(By.CLASS_NAME,"db-view__item__text__name")
            name=namex.text
          except NoSuchElementException:
            name="NULL"
          except StaleElementReferenceException:
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
            continue
          try: 
            categoryx=driver.find_element(By.CLASS_NAME,"db-view__gathering__text__category")
            category=categoryx.text
          except NoSuchElementException:
            category="NULL"
          except StaleElementReferenceException:
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
            continue
          try:
            Glocationx=driver.find_element(By.CLASS_NAME,"db-view__gathering__area")
            Glocation=Glocationx.text
          except NoSuchElementException:
            Glocation="NULL"
          except StaleElementReferenceException:
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
            continue
          try:
            locationx=driver.find_element(By.CLASS_NAME,"db-view__gathering__point")
            location=locationx.text
          except NoSuchElementException:
            location="NULL"
          except StaleElementReferenceException:
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
            continue
          try:
            gatherlst[name]={"job":job, "item_category":category,"Glocation":Glocation, "location":location}
          except:
            self.errvisited.append(vars)
            errorchk=False
            counterr=counterr+1
            continue
      dummy=self.errvisited
      countse=0
      counterr=0
      while(list(self.errvisited)!=[]):
          #3600 seconds is 1 hr
          time.sleep(3600)
          count=1
          while(list(self.errvisited)!=[] and len(dummy)<=count):
            dummy=self.errvisited
            for vars in list(dummy):
                  count=count+1
                  #makes the current scope the page of the new element
                  #also adds a link to a page if its unable to connect where it will attempt again in 1 hr
                  
                  try:
                      driver.get(vars)
                      errorchk=True
                      self.errvisited.remove(vars)
                      dummy=self.errvisited
                      countse=countse+1
                      
                      
                  except:
                      print("there is some issue with connecting to one or more of the items we will retry those missing in 1hr")
                      print("the url that failed is:", vars)
                      errorchk=False
                      counterr=counterr+1
                  if errorchk:
                    try:
                      jobx=driver.find_element(By.CLASS_NAME,"db-view__item__text__job_name")
                      job=[jobx.text]
                    except NoSuchElementException:
                      job="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    #get the name of the item to gather
                    try:
                      namex=driver.find_element(By.CLASS_NAME,"db-view__item__text__name")
                      name=namex.text
                    except NoSuchElementException:
                      name="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    try: 
                      categoryx=driver.find_element(By.CLASS_NAME,"db-view__gathering__text__category")
                      category=categoryx.text
                    except NoSuchElementException:
                      category="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    try:
                      Glocationx=driver.find_element(By.CLASS_NAME,"db-view__gathering__area")
                      Glocation=Glocationx.text
                    except NoSuchElementException:
                      Glocation="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    try:
                      locationx=driver.find_element(By.CLASS_NAME,"db-view__gathering__point")
                      location=locationx.text
                    except NoSuchElementException:
                      location="NULL"
                    except StaleElementReferenceException:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
                    try:
                      gatherlst[name]={"job":job, "item_category":category,"Glocation":Glocation, "location":location}
                    #error wont be based off of selenium for this one so we will post a 
                    except:
                      self.errvisited.append(vars)
                      errorchk=False
                      counterr=counterr+1
                      continue
      #creates an "official" gathering json
      with open("FfxivOfficialGathering.json", "w+") as outfile:
        json.dump(gatherlst, outfile, indent = 6)
        
        
    #goes to the garland api to make a json of all the ways to obtain an item
    #NOTE will run an update for IDDB 
    def garlandResourceObtain(self,listofID=[]):
      if(listofID==[]):
        print("you must supply a list of Item ID's\n run one of the item Sorters first")
      for vars in listofID:
        collectableItemAttr={}
        #try:
        flood={"id":str(vars),"type":"item","lang":"en","version":"3"}
        itemx=requests.get(self.GARLANDAPI, params=flood)
        item=itemx.json()
        collectableItemAttr[vars]=item
        print("conf1")
      
          
        #except:
        print("an error occurred while retrieving information for ", vars)
      with open("collectableItemAttr.json", "w+") as outfile:
        json.dump(collectableItemAttr, outfile, indent = 6)    
      
      
    
    #sorts through a dict of items with items being the topmost keys returns a list of item id's
    #should run updateIDDB first
    def itemSorterDict(self, itemdict):
      outputlist=[]
      with open('itemid.json') as json_file:
          data = json.load(json_file)
    #sorts through the dictionary supplied by the user
      for outer in dict(itemdict):
        found=False    
    #sorts through the dictonary of ffxiv values
        for vars in dict(data):
          if(str((data[vars]).get("en")).lower()==str(outer).lower()):
            found=True
            outputlist.append(vars)
    #if no match was found will return "NULL"
        if(found==False):
          outputlist.append("NULL")
      return(outputlist)
        
    
    #sorts through a list of item names and transforms them to a list of their item id's
    #should run updateIDDB first
    def itemSorterList(self, itemlist):
      outputlist=[]
      with open('itemid.json') as json_file:
        data = json.load(json_file)
    #sorts through the dictionary supplied by the user
      for outer in itemlist:
        found=False    
    #sorts through the dictonary of ffxiv values and assigns them if a match
        for vars in dict(data):
          if(str((data[vars]).get("en")).lower()==str(outer).lower()):
            found=True
            outputlist.append(vars)
    #if no match was found will return "NULL"
        if(found==False):
          outputlist.append("NULL")
      return(outputlist)
        
         
        
scraper=ffxiv_grabber("https://na.finalfantasyxiv.com/lodestone/playguide/db/gathering/?page=1", "https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=1") 
#scraper.ffxivCraftScraper("db-table__txt--detail_link")
#scraper.ffxivGatherScraper("db-table__txt--detail_link")
scraper.updateIDDB()
Dictionary={}
with open('Ffxivcrafting.json') as json_file:
        data = json.load(json_file)
for vars in data:
  Dictionary.update((data[vars]).get("Ingredients"))
id=scraper.itemSorterDict(Dictionary)
scraper.garlandResourceObtain(id)  
