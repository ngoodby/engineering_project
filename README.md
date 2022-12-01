# Metis Engineering Project

*Design*: I brought together weather, tide, and air quality data to create a simple web app for water sports enthusiasts to reference to identify ideal days and times for them to go out on the water. A data pipeline was constructed to allow for easy updating of the data underlying the web application to allow users to view current and forecasted conditions. Increasing access to information on these sorts of conditions makes it easier for people to confidently and safely enjoy water sports. This can help to increase participation and access to water sports, helping to bolster business for any company that makes products to facilitate participation in sports like sailing, paddleboarding, kayaking, and open water swimming. 

*Data*: Data was gathered from through web scraping and the use of three different APIs. Station names and ID numbers of locations in California, Oregon, and Washington with tide stations were scraped from NOAA’s Tides and Currents website. Data was then gathered for these locations on tides, air quality, wind, and precipitation using the following three APIs:
- NOAA Tides and Currents
- OpenWeatherMap Air Pollution
- Weatherbit

*Algorithm*: This project brought together diverse data types using a data pipeline that allows the data to be easily updated and presents the data in an interactive and user friendly manner. No modeling was done for this project.  

*Tools*:
- Requests, Selenium, BeautifulSoup, and MongoDB to get and store location info
- Store data in MongoDB using Pymongo
- Cron to schedule daily data updates
- Streamlit to visualize and interact with data

*Communication*: The data was visualized as a web application using Streamlit and deployed locally. A brief presentation was prepared to communicate the project design and results, which can be found [here]().
