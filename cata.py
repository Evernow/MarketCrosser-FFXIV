from contextlib import nullcontext
import json
with open('CurrentData.json') as json_file:
    source = json.load(json_file)
gil10kj= open("gil10k.json", "w+")
gil100kj= open("gil100k.json", "w+")
gil1mj=open("gil100k.json","w+")
gil10mj=open("gil10m.json","w+")
gilBeyondj=open("gilBeyond.json","w+")

#declares the lists containing the dicts 
gil10k, gil100k, gil1m, gil10m, gilBeyond=[{}]
    
#places each item into a respective price bracket
def catagories():
    #goes thru all items
    for inf in source:
     price = inf["LowestPrice"]
     #sorts out null variables
     if price == nullcontext:
        price=price #does nothing
     elif price <=1000:
         gil10k.append(inf)
     elif price <=10000:
         gil100k.append(inf)
     elif price <=100000:
         gil1m.append(inf)
     elif price <=1000000:
         gil10m.append(inf)
     elif price >1000000:
         gilBeyond.append(inf)
               
    
    
