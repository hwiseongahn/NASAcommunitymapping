import pandas as pd
import folium
m = folium.Map(location=[56.1304, -106.3468], tiles="OpenStreetMap", zoom_start=4)

def get_province_data():
    data = pd.DataFrame({
        'lon': [
            -84.3478,
            -105.0008,
            -123.3656,
            -66.4619,
            -63.1340,
            -97.5500,
            -58.0000,
            -115.5834,
            -135.0000,
            -119.4900,
            -62.8600
        ],
        'lat': [
            50.0000,
            55.0000,
            53.7267,
            46.5653,
            46.5107,
            53.7609,
            53.1355,
            55.0000,
            64.2823,
            64.8255,
            45.0000
        ],
        'name': [
            'Ontario',
            'Saskatchewan',
            'British Columbia',
            'New Brunswick',
            'Prince Edward Island',
            'Manitoba',
            'Newfoundland and Labrador',
            'Alberta',
            'Yukon',
            'Northwest Territories',
            'Nova Scotia'
        ],
        'value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    })
    return data


data = get_province_data()

for i in range(len(data)):
    folium.Marker(
        location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
        popup=f"{data.iloc[i]['name']} - Value: {data.iloc[i]['value']}"
    ).add_to(m)

m.save('canadaMap.html')