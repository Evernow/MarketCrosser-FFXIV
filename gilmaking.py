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
from scipy import stats
from collections import OrderedDict

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
    current_siren_price = None
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
            if (current_siren_price == None) or (listing['pricePerUnit'] < current_siren_price):
                if listing['worldID'] == 57:
                    current_siren_price = listing['pricePerUnit']
    return lowest_price, lowest_price_server, current_siren_price
    # if lowest_price_server == None:
    #     return None
    # return lowest_price,lowest_price_server
    
def AverageSalePrice(item,quality,q):
    # Returns average sales price and average quantiy sold in a sale in the last 4 days
    list_of_sales_price = []
    list_of_sales_quantity = []
    sales_in_last_day = 0
    sales_in_last_week = 0
    sales_in_last_month = 0 
    with open(os.path.join(parent_directory,f"GetNumberOfSales_{item}.json")) as json_file:
        HistoryOfSalesData = json.load(json_file)[str(item)]['entries']
    for sale in HistoryOfSalesData:
        if sale['worldID'] == 57  and sale['hq'] == quality: #and ((time.time()-sale['timestamp'])< 345600):
            if (time.time()-sale['timestamp']) < 604800:
                print('test')
                list_of_sales_quantity.append(sale['quantity'])
                list_of_sales_price.append(sale['pricePerUnit']) 
            if (time.time() - sale['timestamp']) < 86400:
                sales_in_last_day += 1
            if (time.time() - sale['timestamp']) < 604800:
                sales_in_last_week += 1
            if (time.time() - sale['timestamp']) < 2628288:
                sales_in_last_month += 1
    if len(list_of_sales_price) > 0:
        mean_list_price = stats.trim_mean(list_of_sales_price, 0.2)
        mean_list_quantity = mean(list_of_sales_quantity)
    else:
        mean_list_price = None
        mean_list_quantity = None
    minpricedata = minprice(item,quality)
    q[str((item,quality))] =  {'AveragePriceSiren': mean_list_price, 'AverageQuantitySiren': mean_list_quantity, 'CurrentPriceSiren' : minpricedata[2],
                                'LowestPrice': minpricedata[0], 'LowestPriceServer': minpricedata[1],
                                'SalesInLast24Hours': sales_in_last_day, 'SalesInLastWeek': sales_in_last_week,
                                'SalesInLastMonth': sales_in_last_month}
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



testing = False
if __name__ == '__main__':
    if not testing:
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
        multiprocessingdict = dict(multiprocessingdict)
        multiprocessingdict = OrderedDict(sorted(multiprocessingdict.items(), key=lambda t: t[0]))
        with open("CurrentData.json", "w+") as outfile:
            json.dump(multiprocessingdict, outfile, indent = 4)
        files = glob.glob(os.path.join('JobInProgress/', "*"))
        for f in files:
            # If a directory is completely empty github removes it, so we have a dummy file in it always
            if 'dummyfiledonotremove.txt' not in f:
                os.remove(f)



