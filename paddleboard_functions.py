import requests

def get_weather_data(stations):
'''
Retrieve current and forecasted weather.
'''
    weather_list = []
    weather_url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly"
    for station in stations:
        querystring = {"lat":station['lat'],"lon":station['long'],"hours":"72"}
        headers = {
            "X-RapidAPI-Key": "1282a0348bmsh6030279122a830ap16b70fjsn3c47099439d6",
            "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
        }
        weather_dict = {'station_name':station['station_name'],
                        'station_id':station['station_id'],
                        'lat':station['lat'],
                        'long':station['long'],
                        'response':requests.request("GET", weather_url, headers=headers, params=querystring).json()['data']
                       }
        weather_list.append(weather_dict)
    return weather_list

def get_tides_data(stations):
    '''
    Retrieve current and forecasted tides.
    '''
    tides_response = []
    for station in stations:
        tides_url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{}.json?expand=products".format(station['station_id'])
        tides_dict = {'station_name':station['station_name'],
                      'station_id':station['station_id'],
                      'lat':station['lat'],
                      'long':station['long'],
                      'response':requests.request("GET", tides_url).json()
                     }
        tides_response.append(tides_dict)
    return tides_response

def get_air_quality_data(stations):
    '''
    Retrive current and forecasted air quality measures. 
    '''
    aqi_list = []
    for station in stations:
        aqi_url = "http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={}&lon={}&appid={}".format(
            station['lat'], station['long'], '12b57316a4ce5ebac5e0386d9ee999be'
        )
        aqi_dict = {'station_name':station['station_name'],
                    'station_id':station['station_id'],
                    'lat':station['lat'],
                    'long':station['long'],
                    'response':requests.request("GET", aqi_url).json()
             }
        aqi_list.append(aqi_dict)
    print(aqi_url) #checking one output of the url format to make sure it's working smoothly
    return aqi_list
