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
gil10k, gil100k, gil1m, gil10m, gilBeyond=[{}],[{}],[{}],[{}],[{}]
    
#places each item into a respective price bracket
def catagories():
    #goes thru all items
    for inf in source:
     price= source[inf]["LowestPrice"]
     #sorts out null variables
     if price == None:
        price=price #does nothing
     elif price <=1000:
         json.dump(inf,gil10kj, indent = 6)
         json.dump(source[inf],gil10kj, indent = 6)
     elif price <=10000:
        json.dump(inf, gil100kj, indent = 6)
        json.dump(source[inf], gil100kj, indent = 6)
         
     elif price <=100000:
        json.dump(inf, gil1mj, indent = 6)
        json.dump(source[inf], gil1mj, indent = 6)
     elif price <=1000000:
        json.dump(inf, gil10mj, indent = 6)
        json.dump(source[inf], gil10mj, indent = 6)
     elif price >1000000:
        json.dump(inf, gilBeyondj, indent = 6)
        json.dump(source[inf], gilBeyondj, indent = 6)
    #json.dump(gil100k, gil100kj, indent = 6)
    #json.dump(gil1m,gil1mj, indent = 6)
    #json.dump(gil10m,gil10mj,indent =6 )
    #json.dump(gilBeyond,gilBeyondj,indent =6 )
catagories()    
               
    
    
