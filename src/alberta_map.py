import folium
import main
import pandas as pd

def generateAlbertaMap():
    albertamap = folium.Map(location=[56.1304, -90.3468], tiles="OpenStreetMap", zoom_start=7)
    df = pd.read_csv("res/carbonemissions.csv")
    albertamap.save('src/static/albertaMap.html')
