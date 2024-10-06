import folium
import main
import pandas as pd
from folium.plugins import HeatMap, HeatMapWithTime
import json

def generateAlbertaMap(option, year):
    global albertamap
    albertamap = folium.Map(location=[55, -115.5834], tiles="OpenStreetMap", zoom_start=5)
    df = pd.read_csv("res/carbonemissions.csv")
    generate_alberta_heatmap(option, year) 
    albertamap.save('src/static/albertaMap.html')

def generate_alberta_heatmap(option, year):

    data = main.loadJSON(f"res/{option}_{year}_data.json")

    #test source and year
    #set source and year

    if option == "algae":
        algae_values = [float(num["averageCellCount"]) for num in data]
        max_algae = max(algae_values)
    #create a loop that iterates through co2 values, finds the associated "Region" and gets the 'lon' and 'lat' value from
    # the coordinates dataFrame and adds it as a new list into the heat map data list
        heatmap_data = []
        for city in data:
            city_name = city['city_name']

            lat = float(city['latitude'])
            lon = float(city['longitude'])
            value = float(city['averageCellCount'])/max_algae #divide by the max value to get our opacity value between 0 and 1

            # Add the data to heatmap_data
            heatmap_data.append([lat, lon, value])  # Append [latitude, longitude, CO2 value]

    
    #make if statement for CO2
    elif option == "co2":
        co2_values = [float(num["co2_Value"]) for num in data]
        max_co2 = max(co2_values)
    #create a loop that iterates through co2 values, finds the associated "Region" and gets the 'lon' and 'lat' value from
    # the coordinates dataFrame and adds it as a new list into the heat map data list
        heatmap_data = []
        for city in data:
            city_name = city['city_name']

            lat = float(city['latitude'])
            lon = float(city['longitude'])
            value = float(city['co2_Value'])/max_co2 #divide by the max value to get our opacity value between 0 and 1

            # Add the data to heatmap_data
            heatmap_data.append([lat, lon, value])  # Append [latitude, longitude, CO2 value]




    HeatMap(heatmap_data, radius=50, blur=40, min_opacity=0.2).add_to(albertamap)
    
    # for row in data:

    #     lat = row["latitude"]
    #     print(lat)
    #     lon = row["longitude"]
    #     value = row["averageCellCount"]

    #     heatmap_data.append([lat, lon, value])

    # HeatMap(heatmap_data, radius=50, blur=40, min_opacity=0.2).add_to(albertamap)


