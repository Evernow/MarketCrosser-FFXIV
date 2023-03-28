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


def GetNumberOfSales(itemIDs):
    # Returns sales done in the last 24 hours in Siren
    modifyMemoryDict = {}
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
    with open(f"GetNumberOfSales_{itemIDs}.json", "w+") as outfile:
        json.dump(modifyMemoryDict, outfile)




def GetAllMarketableItems():
    api_url = f"https://universalis.app/api/v2/marketable"
    response = requests.get(api_url).json()
    return response

def GetCurrentSaleListings(itemIDs):
    item_world_minimum = {}
    api_url = f"https://universalis.app/api/v2/North-America/{itemIDs}"
    response = requests.get(api_url).json()
    item_world_minimum[str((itemIDs))] = response
    with open(f"GetCurrentSaleListings_{itemIDs}.json", "w+") as outfile:
        json.dump(item_world_minimum, outfile)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
# Get all current items that can be sold
all_marketable_items = GetAllMarketableItems()
# Get all names of items
with open("AllMarketableItems_Encrypted.json", "w") as outfile:
    json.dump(all_marketable_items, outfile)
# name_of_items = requests.get('https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json').json()
if __name__ == '__main__':
    while True:
        try:
            for item in chunker(all_marketable_items, 100):
                jobs = []
                for i in item:
                    try:
                        p = multiprocessing.Process(target=GetNumberOfSales, args=(i,))
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
#                break

            for item in chunker(all_marketable_items, 100):
                jobs = []
                for i in item:
                    try:
                        p = multiprocessing.Process(target=GetCurrentSaleListings, args=(i,))
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
 #               break
            subprocess.run('tar cvf - *.json | gzip -9 - > compressFileName.tar.gz',shell=True)
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                if ('.gz' in f ) and ('compressFileName') not in f:
                    os.remove(f)
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                if ('.json' in f ):
                    os.remove(f)

        except:
            print(str(traceback.format_exc()))
        time.sleep(10800)
