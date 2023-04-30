#a class containing all the convenience interface related functions for autoruning and utilizing different objects 
import json
from ffxiv_info_grabber import ffxiv_grabber
from multipledispatch import dispatch 
class interface:
    
    #if rerun is true it will run the scraper portion of the code with logging disabled and rerunning enabled
    #defaults to false(rerun should be true in server implementations)
    # 1 = minimal, only pulls and updates the api and item DB
    # 2 = standard, scrapes for crafters and updates/pulls the api (no gatherers) as well as the item DB
    # 3 = Extra, scrapes for crafters, gatherers, and the api 
    #@dispatch(scraper=ffxiv_grabber, rerun=bool, typeofrun=int)
    def autorun_grabber(self, scraper, rerun, typeofrun=1):
        #with automatic redo
        match typeofrun:
            #if option 2 is chosen:
            case 2:
                if rerun:
                    scraper.ffxivCraftScraper("db-table__txt--detail_link")
                else: 
                    scraper.ffxivCraftScraper("db-table__txt--detail_link",False)  
            #if option 3 is chosen:
            case 3:
                if rerun:
                    scraper.ffxivGatherScraper("db-table__txt--detail_link")
                    scraper.ffxivCraftScraper("db-table__txt--detail_link")
                else:
                    scraper.ffxivGatherScraper("db-table__txt--detail_link",False)
                    scraper.ffxivCraftScraper("db-table__txt--detail_link",False)
        scraper.updateIDDB()
        Dictionary={}
        with open('Ffxivcrafting.json') as json_file:
                data = json.load(json_file)
        #grabs all the items needed to translate
        for vars in data:
            Dictionary.update((data[vars]).get("Ingredients"))
        listofitemid=scraper.itemSorter(Dictionary)
        #dump file for troubleshooting by user
        with open("dump.json", "w+") as outfile:
            json.dump(listofitemid, outfile, indent = 6) 
        if rerun:
            scraper.garlandResourceObtain(listofitemid, True)
        else:
            scraper.garlandResourceObtain(listofitemid, True)
                       
                        
    def autorun_gilmaking(rerun=False):
        return()