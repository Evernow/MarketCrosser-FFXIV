# Trying to make gil

import requests # pip install requests
import time
import sys
import json
import traceback
import multiprocessing
import os
import subprocess

world_IDs = {73: 'Adamantoise', 79: 'Cactuar', 54: 'Faerie', 63: 'Gilgamesh', 40: 'Jenova', 65: 'Midgardsormr', 99: 'Sargatanas', 57: 'Siren',
            34: 'Brynhildr', 37: 'Mateus', 41: 'Zalera', 62: 'Diabolos', 74: 'Coeurl', 75: 'Malboro', 81: 'Goblin', 91: 'Balmung', 
            35: 'Famfrit', 53: 'Exodus', 55: 'Lamia', 64: 'Leviathan', 77: 'Ultros', 78: 'Behemoth', 93: 'Excalibur', 95: 'Hyperion', 
            404: 'Marilith', 405: 'Seraph', 406: 'Halicarnassus', 407: 'Maduin'}



def GetNumberOfSales(itemIDs,modifyMemoryDict):
    # Returns sales done in the last 24 hours in Siren
    api_url = f"https://universalis.app/api/v2/history/North-America/{itemIDs}?entriesToReturn=999"
    # print(api_url)
    attempts = 0
    while attempts < 20:
        try:
            response = requests.get(api_url,timeout=60).json()
            break
        except:
            attempts +=1
            time.sleep(1)
    if attempts > 19:
        modifyMemoryDict[str((response['itemID']))] = None 
        return
    modifyMemoryDict[str((response['itemID']))] = response

        

def GetAllMarketableItems():
    api_url = f"https://universalis.app/api/v2/marketable"
    response = requests.get(api_url).json()
    return response

def GetCurrentSaleListings(itemIDs,item_world_minimum):
    api_url = f"https://universalis.app/api/v2/North-America/{itemIDs}"
    response = requests.get(api_url).json()
    item_world_minimum[str((itemIDs))] = response

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
# Get all current items that can be sold
all_marketable_items = GetAllMarketableItems()
# Get all names of items
with open("AllMarketableItems_Encrypted.json", "w") as outfile:
    json.dump(all_marketable_items, outfile)
# name_of_items = requests.get('https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json').json()
if __name__ == '__main__':
    try:
        manager = multiprocessing.Manager()
        HistoryOfSalesData = manager.dict()
        for item in chunker(all_marketable_items, 10):
            jobs = []
            for i in item:
                try:
                    p = multiprocessing.Process(target=GetNumberOfSales, args=(i,HistoryOfSalesData,))
                    jobs.append(p)
                    p.start()
                except:
                    print("Couldn't process item " + str(i))   
                    print(traceback.format_exc())
            while len(jobs) > 0:
                jobs = [job for job in jobs if job.is_alive()]
                time.sleep(1)
            print('Finished a batch of jobs')
            print(f'{item[0]} to {item[-1]}')

        json_object = json.dumps(dict(HistoryOfSalesData), indent=4)
        with open("HistoryOfSalesData_Encrypted.json", "w") as outfile:
            json.dump(json_object, outfile)
        CurrentSalesData = manager.dict()
        for item in chunker(all_marketable_items, 10):
            jobs = []
            for i in item:
                try:
                    p = multiprocessing.Process(target=GetCurrentSaleListings, args=(i,CurrentSalesData,))
                    jobs.append(p)
                    p.start()
                except:
                    print("Couldn't process item " + str(i))   
                    print(traceback.format_exc())
            while len(jobs) > 0:
                jobs = [job for job in jobs if job.is_alive()]
                time.sleep(1)
            print('Finished a batch of jobs')
            print(f'{item[0]} to {item[-1]}')
        json_object = json.dumps(dict(CurrentSalesData), indent=4)
        with open("CurrentSalesData_Encrypted.json", "w") as outfile:
            json.dump(json_object, outfile)

    # Encrypts file, this is so we don't have this sort of raw data open in the github, potentially attracting copyright trolls.
    except:
        print(str(traceback.format_exc()))
