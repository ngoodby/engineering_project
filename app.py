import streamlit as st
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime
import pydeck as pdk

client = MongoClient()
# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_data(col):
    db = client.paddleboard
    items = db[col].find()
    items = list(items)  # make hashable for st.experimental_memo
    return items
aqi_data = get_data('aqi')
weather_data = get_data('weather')
tides_data = get_data('tides')

st.title("Conditions on the Water")

#choices
location_name = st.sidebar.selectbox("Select Location", 
	[item['station_name'] for item in aqi_data]
	)
times = [i['dt'] for i in aqi_data['station_name'==location_name]['response']['list']]
times = pd.to_datetime(times, unit='s', origin='unix')
today = np.min(times.date)
end_date = today + datetime.timedelta(days=3)
d = st.sidebar.slider("Select Date of Interest", today, end_date)

#aqi info
aqi = [i['main']['aqi'] for i in aqi_data['station_name' == location_name]['response']['list']]
t_aqi = list(zip(times.date, aqi))
aqi_display = [i[1] for i in t_aqi if i[0]==d]
aqi_dict = {1:'GOOD', 2: 'FAIR', 3:'MODERATE', 4:'POOR', 5:'VERY POOR'}
st.write(f"#### Air Quality Index (AQI) on {d} at {location_name} is {aqi_dict[np.max(aqi_display)]}")

#tides
st.write(f"#### View tidal predictions for this location [here]({tides_data[0]['response']['stations'][0]['products']['products'][0]['value']})")
col1, col2 = st.columns(2)

with col1:
    st.header("Wind")
with col2:
    st.header("Temperature")
font = {'family' : 'Source Sans Pro',
        'size'   : 24}

plt.rc('font', **font)

#wind
weather = weather_data['station_name'==location_name]['response']
wind = [i['wind_spd'] for i in weather]
date_times = [i['datetime'].split(":") for i in weather]
date = pd.to_datetime([i[0] for i in date_times])
hour = pd.Series([i[1] for i in date_times])
date_times = date + hour.astype("timedelta64[h]")
wind_dict = {'dts':date_times, 'wind':wind}
wind_df = pd.DataFrame(wind_dict)
wind_df_filtered = wind_df[wind_df.dts.dt.date == d]
fig = plt.figure()
plt.plot(wind_df_filtered.dts, wind_df_filtered.wind)
ax = plt.gca()
ax.set_ylabel('Wind Speed (MPH)')
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I%p'))
plt.gcf().autofmt_xdate(rotation = 90)
col1.pyplot(fig)

#temp
temp = [i['temp'] for i in weather]
temp = [i*(9/5)+32 for i in temp]
temp_dict = {'dts':date_times, 'temp':temp}
temp_df = pd.DataFrame(temp_dict)
temp_df_filtered = temp_df[temp_df.dts.dt.date == d]
fig = plt.figure()
plt.plot(temp_df_filtered.dts, temp_df_filtered.temp)
ax = plt.gca()
ax.set_ylabel('Temperature (ºF)')
ax.xaxis.set_major_locator(mdates.HourLocator(interval = 4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I%p'))
plt.gcf().autofmt_xdate(rotation = 90)
col2.pyplot(fig)

#map
lats = [float(i['lat']) for i in aqi_data]
longs = [float(i['long']) for i in aqi_data]
latlongs_df = pd.DataFrame(list(zip(lats,longs)), columns = ['lat','lng'])
latlong = [i for i in aqi_data if i['station_name']==location_name]
latlong = [float(latlong[0]['lat']), float(latlong[0]['long'])]
df = pd.DataFrame([latlong], columns=['lat','lng'])

pdk_object = pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=47,
         longitude=-123,
         pitch=30,
         zoom=6
     ),
     layers = [pdk.Layer(
        'ScatterplotLayer',
        data = latlongs_df,
        get_position=['lng', 'lat'],
        auto_highlight=True,
        get_radius=2500,
        get_fill_color='[75,205,250]'
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data = df,
            get_position = ['lng','lat'],
            auto_highlight=True,
            get_radius=5000,
            get_fill_color='[255,94,87]'
            )
            ]
            )
st.pydeck_chart(pdk_object)