#a class containing all the interface related functions for different objects 
import json
from ffxiv_info_grabber import ffxiv_grabber
class interface:
    def autorun_grabber(rerun):
        if rerun: 
            scraper=ffxiv_grabber("https://na.finalfantasyxiv.com/lodestone/playguide/db/gathering/?page=1", "https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=1") 
            #with automatic redo
            scraper.ffxivCraftScraper("db-table__txt--detail_link")
            scraper.ffxivGatherScraper("db-table__txt--detail_link")
            scraper.updateIDDB()
            Dictionary={}
            with open('Ffxivcrafting.json') as json_file:
                    data = json.load(json_file)
            #grabs all the items needed to translate
            for vars in data:
                Dictionary.update((data[vars]).get("Ingredients"))
            id=scraper.itemSorter(Dictionary)
            with open("dump.json", "w+") as outfile:
                json.dump(id, outfile, indent = 6)    
            scraper.garlandResourceObtain(id)  
        else:
            #EXAMPLE IMPLEMENTATION  
            scraper=ffxiv_grabber("https://na.finalfantasyxiv.com/lodestone/playguide/db/gathering/?page=1", "https://na.finalfantasyxiv.com/lodestone/playguide/db/recipe/?page=1") 
            #without automatic redo but now with error logging
            scraper.ffxivCraftScraper("db-table__txt--detail_link",False)
            scraper.ffxivGatherScraper("db-table__txt--detail_link",False)
            scraper.updateIDDB()
            Dictionary={}
            with open('Ffxivcrafting.json') as json_file:
                    data = json.load(json_file)
            #grabs all the items needed to translate
            for vars in data:
                Dictionary.update((data[vars]).get("Ingredients"))
            id=scraper.itemSorter(Dictionary)
            with open("dump.json", "w+") as outfile:
                json.dump(id, outfile, indent = 6)    
            scraper.garlandResourceObtain(id)  


        
        