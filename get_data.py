import requests
import pymongo
from pymongo import MongoClient
from paddleboard_functions import get_weather_data, get_tides_data, get_air_quality_data

#retrive list of station names and IDs to use for data queries.
client = MongoClient()
station_info_db = client["stations"]
station_info = station_info_db['station_info']
cursor = station_info.find()
stations = list(cursor)

#clear out old data
client.drop_database('paddleboard')
database_list = client.database_names()
print ("db names:", database_list)

#collect and load new data into MongoDB
weather_data = get_weather_data(stations)
db = client["paddleboard"]
weather = db["weather"]
weather.insert_many(weather_data)

get_tides_data(stations)
tides = db["tides"]
tides.insert_many(tides_data)

aqi_data = get_air_quality_data(stations)
aqi = db["aqi"]
aqi.insert_many(aqi_data)

print("Databases:", client.list_database_names())
print("Collections:", db.list_collection_names())