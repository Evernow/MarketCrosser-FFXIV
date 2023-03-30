# Trying to make gil
from urllib.request import urlopen, Request
import time
import sys
import json
import traceback
import multiprocessing
import os
import shutil
from datetime import datetime
from ftplib import FTP
import io
import glob
import os
import traceback
import multiprocessing
import time
import tarfile
import cProfile
import pstats
import io
from pstats import SortKey

from statistics import mean 
world_IDs = {73: 'Adamantoise', 79: 'Cactuar', 54: 'Faerie', 63: 'Gilgamesh', 40: 'Jenova', 65: 'Midgardsormr', 99: 'Sargatanas', 57: 'Siren',
            34: 'Brynhildr', 37: 'Mateus', 41: 'Zalera', 62: 'Diabolos', 74: 'Coeurl', 75: 'Malboro', 81: 'Goblin', 91: 'Balmung', 
            35: 'Famfrit', 53: 'Exodus', 55: 'Lamia', 64: 'Leviathan', 77: 'Ultros', 78: 'Behemoth', 93: 'Excalibur', 95: 'Hyperion', 
            404: 'Marilith', 405: 'Seraph', 406: 'Halicarnassus', 407: 'Maduin'}
# if os.name == 'nt':
#     parent_directory = r"C:\Users\Daniel\Desktop\FTPTest"
# else:
parent_directory = "JobInProgress"
def minprice(item,quality):
    # Returns lowest price the item is selling at and its respective server
    returndict = {}
    lowest_price = None
    lowest_price_server = None
    current_siren_price = sys.maxsize-1
    with open(os.path.join(parent_directory,f"GetCurrentSaleListings_{item}.json")) as json_file:
        CurrentSalesData = json.load(json_file)[str(item)]['listings']
    for listing in CurrentSalesData:
        if (listing['hq'] == quality) and (listing['worldID'] in world_IDs.keys()):
            if lowest_price == None:
                lowest_price = listing['pricePerUnit']
                lowest_price_server = listing['worldName']
            elif listing['pricePerUnit'] < lowest_price:
                    lowest_price = listing['pricePerUnit']
                    lowest_price_server = listing['worldName']
            if (listing['worldID'] == 57) and (listing['pricePerUnit'] < current_siren_price):
                current_siren_price = listing['pricePerUnit']
    return lowest_price, lowest_price_server, current_siren_price
    # if lowest_price_server == None:
    #     return None
    # return lowest_price,lowest_price_server
    
def AverageSalePrice(item,quality,q):
    # Returns average sales price and average quantiy sold in a sale in the last 4 days
    list_of_sales_price = []
    list_of_sales_quantity = []
    with open(os.path.join(parent_directory,f"GetNumberOfSales_{item}.json")) as json_file:
        HistoryOfSalesData = json.load(json_file)[str(item)]['entries']
    for sale in HistoryOfSalesData:
        if sale['worldID'] == 57  and sale['hq'] == quality: #and ((time.time()-sale['timestamp'])< 345600):
            list_of_sales_quantity.append(sale['quantity'])
            list_of_sales_price.append(sale['pricePerUnit']) 
    if len(list_of_sales_price) > 0:
        mean_list_price = mean(list_of_sales_price)
        mean_list_quantity = mean(list_of_sales_quantity)
    else:
        mean_list_price = None
        mean_list_quantity = None
    minpricedata = minprice(item,quality)
    q[str((item,quality))] =  {'AveragePriceSiren': mean_list_price, 'AverageQuantitySiren': mean_list_quantity, 'CurrentPriceSiren' : minpricedata[2],
                                'LowestPrice': minpricedata[0], 'LowestPriceServer': minpricedata[1]}
    return

def chunker(seq, size):
    # Used for multiprocessing, don't remember how it works, been copy pasting it for years now
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def GetAllMarketableItems():
    print('called')
    url = f"https://universalis.app/api/v2/marketable"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=url, headers=headers) 
    html = urlopen(req).read() 
    data_json = json.loads(html)
    return data_json


if __name__ == '__main__':
    all_marketable_items = GetAllMarketableItems()#[:10] # Slice is for testing
    q = multiprocessing.Manager()

    multiprocessingdict = q.dict()
    print('Started')
    print('Initialized initial dict')
    for item in chunker(all_marketable_items, 50):
        jobs = []
        for i in item:
            try:
                p = multiprocessing.Process(target=AverageSalePrice, args=(i,False,multiprocessingdict,))
                jobs.append(p)
                p.start()
                p2 = multiprocessing.Process(target=AverageSalePrice, args=(i,True,multiprocessingdict,))
                jobs.append(p2)
                p2.start()
            except:
                print("Couldn't process item " + str(i))   
                print(traceback.format_exc())
        while len(jobs) > 0:
            jobs = [job for job in jobs if job.is_alive()]
        print('Finished a batch of jobs')
        print(f'{item[0]} to {item[-1]}')
        # q.put(None) # This cost me an hour of my life to figure out, if you don't send it a None it'll keep waiting for all eternity.
        # modified_data = {}
        # while True:
        #     item = q.get()
        #     if item is None:
        #         break
        #     modified_data.update(item)
        # multiprocessingdict = multiprocessingdict | modified_data
    multiprocessingdict = dict(multiprocessingdict)
    with open("CurrentData.json", "w+") as outfile:
        json.dump(multiprocessingdict, outfile, indent = 4)
    files = glob.glob('JobInProgress/')
    for f in files:
        # If a directory is completely empty github removes it, so we have a dummy file in it always
        if 'dummyfiledonotremove.txt' not in f:
            os.remove(f)
    # print(multiprocessingdict)











# print(minprice(33696,True))


# matser_dict = {}

# # with open(os.path.join(parent_directory,"HistoryOfSalesData_Encrypted.json")) as json_file:
# #     HistoryOfSalesData = json.load(json_file)
# with open(os.path.join(parent_directory,"CurrentSalesData_Encrypted.json")) as json_file:
#     CurrentSalesData = json.load(json_file)
# print('Finished loading in jsons')
# for item in CurrentSalesData:
#     print(item)
#     item_lowest_location = (maxprice(CurrentSalesData[item])) 
#     siren_prices = CurrentSalesData[item]['Siren']
#     try:
#         last24hourssales = HistoryOfSalesData[item]
#     except KeyError:
#         last24hourssales = 0
#         print(f'No sales found for {item}')
#     if ((siren_prices) != None) and ((item_lowest_location)[1] != None):
#         matser_dict[item] = [item_lowest_location, siren_prices, last24hourssales]
# list_of_differences = []
# current_biggest_dif = 0
# item_name = None
# tupletest = None
# # print(matser_dict)

# for item in matser_dict:
#     # if (matser_dict[item][1] - matser_dict[item][0][0]) * matser_dict[item][2]  > current_biggest_dif:
#         if matser_dict[item][2] > 10:
#             current_biggest_dif = (matser_dict[item][1] - matser_dict[item][0][0]) #* matser_dict[item][2]
#             item_name = item
#             tupletest = matser_dict[item][0]
#             list_of_differences.append((current_biggest_dif,item,matser_dict[item][0],matser_dict[item][1],matser_dict[item][2]))
# # print(current_biggest_dif)
# # print(name_of_items[item_name])
# list_of_differences = sorted(list_of_differences,key=lambda x: x[0],reverse=True
# )
# for x in range(50):
#     # print(f'Item {list_of_differences[x][1]} sells for {list_of_differences[x][3]} in Siren and for {list_of_differences[x][2]} and has sold {list_of_differences[x][4]} times')
#     print()

