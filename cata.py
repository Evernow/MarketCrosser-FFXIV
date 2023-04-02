import json
from urllib.request import urlopen, Request
#declares the lists containing the dicts 
gil10k, gil100k, gil1m, gil10m, gilBeyond30m, gil500k={},{},{},{},{},{}


#places each item into a respective price bracket
def catagories():
   with open('CurrentData.json') as json_file:
      source = json.load(json_file)
   gil10kj= open("gil10k.json", "w+")
   gil100kj= open("gil100k.json", "w+")
   gil1mj=open("gil1m.json","w+")
   gil10mj=open("gil10m.json","w+")
   gilBeyond30mj=open("gilBeyond30m.json","w+")
   gil500kj=open("gil500k.json","w+")

   #goes thru all items
   for inf in source:
      price= source[inf]["LowestPrice"]
      #sorts out null variables
      if price == None:
         continue #does nothing
      #sorts thru everything and puts them into their own respective jsons based on price
      elif price >30000000:
         gilBeyond30m[inf] = source[inf]
      elif price >=10000000:
         gil10m[inf] = source[inf]
      elif price >=1000000:
         gil1m[inf] = source[inf]
      elif price >=500000:
         gil500k[inf] = source[inf]
      elif price >=100000:
         gil100k[inf] = source[inf]
      elif price >=10000:
         gil10k[inf] = source[inf] 
 #puts everything into the jsons
   json.dump(gil10k,gil10kj, indent = 6)
   json.dump(gil100k, gil100kj, indent = 6)
   json.dump(gil500k,gil500kj,indent =6 )
   json.dump(gil1m,gil1mj, indent = 6)
   json.dump(gil10m,gil10mj,indent =6 )
   json.dump(gilBeyond30m,gilBeyond30mj,indent =6 )
   

def GetLowestMarketTax():
   # Gets current lowest tax rate in Siren
   url = f"https://universalis.app/api/v2/tax-rates?world=Siren"
   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
   req = Request(url=url, headers=headers) 
   html = urlopen(req).read() 
   data_json = json.loads(html)
   return min(list(data_json.values()))*0.01

def GetItemNames():
   # Gets current lowest tax rate in Siren
   url = f"https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json"
   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
   req = Request(url=url, headers=headers) 
   html = urlopen(req).read() 
   data_json = json.loads(html)
   return data_json

def SortItemsByValue():
   MarketTax = GetLowestMarketTax()
   sorted_dict = {}
   itemnames = GetItemNames()
   buckets = ["gil10k.json","gil100k.json","gil500k.json","gil1m.json","gil10m.json","gilBeyond30m.json"]
   for bucket in buckets:
      sorted_dict[bucket] = []
      with open(bucket, 'r') as j:
         contents = json.loads(j.read())
      for i in contents:
         index = i 
         i = contents[i]
         try:
            #  ((AveragePriceSiren - (AveragePriceSiren * MarketTax )) - LowestPrice) * SalesInLastMonth * AverageQuantitySiren
            formula =  (((min(i['AveragePriceSiren'], i['CurrentPriceSiren']) - (min(i['AveragePriceSiren'], i['CurrentPriceSiren']) * MarketTax )) - (i['LowestPrice'])) )* i['SalesInLastMonth'] * i['AverageQuantitySiren']
            valueused = round(min(i['AveragePriceSiren'], i['CurrentPriceSiren']),0)
            nameofitem = itemnames[index[index.find('(')+1:index.find(' ')-1]]['en']
            if 'True' in index:
               hq = 'HQ'
            else:
               hq = 'NQ'
            string_readable = f"{nameofitem} ({hq}) sells for {i['LowestPrice']} in {i['LowestPriceServer']} and for {valueused} in Siren, with {i['SalesInLastMonth']} in last month"
            sorted_dict[bucket].append((formula,string_readable))
         except TypeError:
            pass
      sorted_dict[bucket] = sorted(sorted_dict[bucket], key=lambda x: x[0], reverse=True)
   json.dump(sorted_dict,open("ValuesSorted.json", "w+"),indent =1 )
catagories()  
SortItemsByValue()
  
               
    
    
