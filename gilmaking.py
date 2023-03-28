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
if os.name == 'nt':
    parent_directory = r"C:\Users\Daniel\Desktop\FTPTest"
else:
    parent_directory = ""
def minprice(item,quality,multiprocessingdict):
    # Returns lowest price the item is selling at and its respective server
    lowest_price = None
    lowest_price_server = None
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

    multiprocessingdict[str((item,quality))]['LowestPrice'] = lowest_price
    multiprocessingdict[str((item,quality))]['LowestPriceServer'] = lowest_price_server
    return
    # if lowest_price_server == None:
    #     return None
    # return lowest_price,lowest_price_server
    
def AverageSalePrice(item,quality,multiprocessingdict):
    # Returns average sales price and average quantiy sold in a sale in the last 48 hours
    list_of_sales_price = []
    list_of_sales_quantity = []
    with open(os.path.join(parent_directory,f"GetNumberOfSales_{item}.json")) as json_file:
        HistoryOfSalesData = json.load(json_file)[str(item)]['entries']

    for sale in HistoryOfSalesData:
        if sale['worldID'] == 57 and ((time.time()-sale['timestamp'])< 172800) and sale['hq'] == quality:
            list_of_sales_quantity.append(sale['quantity'])
            list_of_sales_price.append(sale['pricePerUnit'])
    if len(list_of_sales_price) == 0:
        return None
    print(mean(list_of_sales_price))
    print(multiprocessingdict[str((item,quality))])
    multiprocessingdict[str((item,quality))]['AveragePriceSiren'] = mean(list_of_sales_price)
    multiprocessingdict[str((item,quality))]['AverageQuantitySiren'] = mean(list_of_sales_quantity)
    print(multiprocessingdict[str((item,quality))]['AveragePriceSiren'])
    # return(mean(list_of_sales_price), mean(list_of_sales_quantity))
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

    # ob = cProfile.Profile()
    # ob.enable()


    # Gets all items that can be sold in a list

    all_marketable_items = GetAllMarketableItems()
    multiprocessingdict = multiprocessing.Manager().dict()
    print('Started')
    for item in all_marketable_items:
        multiprocessingdict[str((item,False))] = {}
        multiprocessingdict[str((item,True))] = {}
        break
    print('Initialized initial dict')
    for item in chunker(all_marketable_items, 1):
        jobs = []
        for i in item:
            try:
                # Average sale price of low quality
                p = multiprocessing.Process(target=AverageSalePrice, args=(i,False,multiprocessingdict,))
                jobs.append(p)
                p.start()
                 # Average sale price of high quality
                p2 = multiprocessing.Process(target=AverageSalePrice, args=(i,True,multiprocessingdict))
                jobs.append(p2)
                p2.start()
                 # Lowest sale price of low quality
                p3 = multiprocessing.Process(target=minprice, args=(i,False,multiprocessingdict))
                jobs.append(p3)
                p3.start()
                 # Highest sale price of high quality
                p4 = multiprocessing.Process(target=minprice, args=(i,True,multiprocessingdict))
                jobs.append(p4)
                p4.start()
            except:
                print("Couldn't process item " + str(i))   
                print(traceback.format_exc())
        while len(jobs) > 0:
            jobs = [job for job in jobs if job.is_alive()]
        break
        print('Finished a batch of jobs')
        print(f'{item[0]} to {item[-1]}')
    print(multiprocessingdict)



    # ob.disable()
    # sec = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(ob, stream=sec).sort_stats(sortby)
    # ps.print_stats()
    # print(sec.getvalue())







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

