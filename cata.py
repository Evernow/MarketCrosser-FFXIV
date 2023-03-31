from contextlib import nullcontext
import json
with open('CurrentData.json') as json_file:
    source = json.load(json_file)
gil10kj= open("gil10k.json", "w+")
gil100kj= open("gil100k.json", "w+")
gil1mj=open("gil1m.json","w+")
gil10mj=open("gil10m.json","w+")
gilBeyondj=open("gilBeyond.json","w+")

#declares the lists containing the dicts 
gil10k, gil100k, gil1m, gil10m, gilBeyond=[],[],[],[],[]
    
#places each item into a respective price bracket
def catagories():
    #goes thru all items
    for inf in source:
     price= source[inf]["LowestPrice"]
     #sorts out null variables
     if price == None:
        continue #does nothing
      #sorts thru everything and puts them into their own respective jsons based on price
      #note that this brings them into a list not a dict
     elif price <=1000:
         gil10k.append({inf:source[inf]})
     elif price <=10000:
         gil100k.append({inf:source[inf]})
     elif price <=100000:
         gil1m.append({inf:source[inf]})
     elif price <=1000000:
         gil10m.append({inf:source[inf]})
     elif price >1000000:
         gilBeyond.append({inf:source[inf]})
 #puts everything into the jsons
    json.dump(gil10k,gil10kj, indent = 6)
    json.dump(gil100k, gil100kj, indent = 6)
    json.dump(gil1m,gil1mj, indent = 6)
    json.dump(gil10m,gil10mj,indent =6 )
    json.dump(gilBeyond,gilBeyondj,indent =6 )
catagories()    
               
    
    
