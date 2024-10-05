import pandas as pd
import folium
m = folium.Map(location=[56.1304, -106.3468], tiles="OpenStreetMap", zoom_start=4)

def get_province_data():
    data = pd.DataFrame({
        'lon': [
            -79.3832,   # Ontario
            -106.3468,  # Saskatchewan
            -123.1216,  # British Columbia
            -66.4619,   # New Brunswick
            -66.6484,   # Prince Edward Island
            -91.2145,   # Manitoba
            -57.6604,   # Newfoundland and Labrador
            -97.7430,   # Alberta
            -126.3469,  # Yukon
            -111.6585   # Northwest Territories
        ],
        # same structure for lat
        'lat': [
            43.6532,  
            52.9399,  
            49.2827, 
            45.2733,  
            46.5653,  
            53.7609,  
            52.9399, 
            53.5461,  
            60.7212, 
            53.9333   
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
            'Northwest Territories'
        ],
        'value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })
    return data

data = get_province_data()

for i in range(len(data)):
    folium.Marker(
        location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
        popup=f"{data.iloc[i]['name']} - Value: {data.iloc[i]['value']}"
    ).add_to(m)

m.save('canadaMap.html')