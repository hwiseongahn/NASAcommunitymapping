import folium
import main
import pandas as pd

def generateAlbertaMap(option, year, data):
    albertamap = folium.Map(location=[56.1304, -90.3468], tiles="OpenStreetMap", zoom_start=7)
    df = pd.read_csv("res/carbonemissions.csv")
    generate_alberta_heatmap(option, year, data) 
    albertamap.save('src/static/albertaMap.html')

def generate_alberta_heatmap(option, year, data):
    return 0

