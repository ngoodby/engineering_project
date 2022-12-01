from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

def get_stations(soup):
    '''
    Get station names for all stations of interest.
    '''
    stations = []
    for ele in soup.find_all(class_ = 'stationname'):
        stations.append(ele.find('a').string)
    return stations

def get_station_ids(soup):
    '''
    Get station ID numbers for all stations of interest.
    '''
    station_ids = []
    for ele in soup.find_all(class_ = 'stationid'):
        station_ids.append(ele.text)
    return station_ids
    
def get_lats(soup):
    '''
    Get latitude for all stations of interest.
    '''
    lats = []
    for ele in soup.find_all(class_ = 'latitude'):
        lats.append(ele.text)
        lats = [lat.replace("+","") for lat in lats]
    return lats

def get_longs(soup):
    '''
    Get longitude for all stations of interest.
    '''
    longs = []
    for ele in soup.find_all(class_ = 'longitude'):
        longs.append(ele.text)
    return longs

#URLs for tide stations in California, Oregon, and Washington.
url_list = ['https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1393#listing', 
            'https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1409#listing',
           'https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1415#listing']
station_dict = {}
for url in url_list:
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    station_dict['station_name'] = get_stations(soup)
    station_dict['station_id'] = get_station_ids(soup)
    station_dict['lat'] = get_lats(soup)
    station_dict['long'] = get_longs(soup)
    driver.execute_script("window.stop();")

assert len(station_dict['station_name'])==len(station_dict['station_id']) == \
len(station_dict['lat']) == len(station_dict['long']), \
f"Lengths of dictionary elements differ: \n\
Num Station Names: {len(station_dict['station_name'])} \n\
Num Station Ids: {len(station_dict['station_id'])} \n\
Num Latitudes: {len(station_dict['lat'])} \n\
Num Longitudes: {len(station_dict['long'])}"

stations = []
for idx, val in enumerate(station_dict['station_name']):
    dict_to_append = {'station_name':station_dict['station_name'][idx],
                      'station_id':station_dict['station_id'][idx],
                      'lat':station_dict['lat'][idx],
                      'long':station_dict['long'][idx]
                      }
    stations.append(dict_to_append)

#store collected data in MongoDB
client = MongoClient()
db = client["stations"]
stations_col = db["station_info"]
stations_col.insert_many(stations)
print("Databases:", client.list_database_names())
print("Collections:", db.list_collection_names())