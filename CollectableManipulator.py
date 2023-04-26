from ffxiv_info_grabber import ffxiv_grabber
import json
import requests
#NOTE data may be inaccurate if ffxiv_grabber was not run recetly
class CollectablesParser:
    def item_elaboration_by_name(self,Name):
        with open('collectableItemAttr.json') as json_file:
            data = json.load(json_file)
        item={}
        stuff=False
        #rotatethrough the values until a matching solution is found. 
        for layr2 in dict(data):
            current=data[layr2]["item"].get("name")
            if(current==Name):
                stuff=True
                item=data[layr2]
                break
        if stuff==True:
        #    print(item)
            return(item)
        else:
            print("error, invalid string")
            
                
                
#stuff=CollectablesParser()
#stuff.item_elaboration_by_name("Maple Lo")