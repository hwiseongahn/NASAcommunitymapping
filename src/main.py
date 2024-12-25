import os
from flask import Flask, render_template, request
import pandas as pd
import folium
import branca
from jinja2 import Template
from folium.plugins import HeatMap
from choropleth import generate_choropleth
import json
from branca.element import Template
import alberta_map
import json

#test comment

def loadJSON(file): #kevin 
    with open(file, 'r') as file:
        data = json.load(file)
    return data

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route("/", methods=["GET", "POST"])
def index():
    map_file = None
    return render_template("index.html", map_file=map_file)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Make sure PORT is set
    app.run(host='0.0.0.0', port=port)  # Use 0.0.0.0 to allow external access

@app.route("/alberta", methods=["POST"])
def alberta():
    map_file = 'albertaMap.html'
    alberta_map.generateAlbertaMap('algae', 2019)
    return render_template("alberta.html", map_file=map_file)

@app.route("/generateAlberta", methods=["POST"])
def generateAlberta():

    option = request.form['option']
    year = int(request.form['year'])
    map_file = 'albertaMap.html'
    alberta_map.generateAlbertaMap(option, year)
    return render_template("alberta.html", map_file=map_file)

@app.route("/canada", methods=["POST"])
def canada():
    map_file = None
    source = 'Agriculture'   
    year = 2020
    

    # Get the province data
    data = get_province_data()

    global m
    # Clear the map before generating a new one
    m = folium.Map(location=[56.1304, -90.3468], tiles="OpenStreetMap", zoom_start=3)

    generate_heatmap(source, year, data,m)  # Generate heatmap based on user input
    generate_markers(data,m)  # Add markers based on the updated data

    # Save the map to a static file
    map_file = 'canadaMap.html'
    m.save(f"src/static/{map_file}")

    return render_template("index.html", map_file=map_file)


@app.route("/generate", methods=["POST"])
def generate():
    map_file = None
    source = request.form['source']    
    year = int(request.form['year'])
    map_to_generate = request.form.get('map_type')#get the button that was clicked to decide which map to generate
    # Get the province data
    data = get_province_data()

    # Clear the map before generating a new one
    m = folium.Map(location=[56.1304, -106.3468], tiles="OpenStreetMap", zoom_start=3)

    #check whether to generate a heatmap or a chloropleth map
    if map_to_generate == 'heatmap':
        generate_heatmap(source, year, data, m)  # Generate heatmap based on user input
        generate_markers(data,m)  # Add markers based on the updated data
    else:
        generate_choropleth(source,year,data,m)

    

    # Save the map to a static file
    map_file = 'canadaMap.html'
    m.save(f"src/static/{map_file}")

    return render_template("index.html", map_file=map_file, selected_source=source, selected_year=year)


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
        'value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
        'co2_value': [0] * 11, #initliaze empty co2 vals
        'current_year': 2024, #default year
        'current_source': 'Agriculture' #default source
    })
    return data



def generate_heatmap(source, year, data, m):
    df = pd.read_csv("res/carbonemissions.csv")

    #test source and year
    #set source and year 
    data['current_year'] = year #set the year so we can access it for the marker
    data['current_source'] = source #set the source so we can access it for the marker
    filtered_rows = df.loc[(df["Source"] == source)
                       & (df["Year"] == year)
                       & (df["Total"] == "y")
                       & (df["Region"] != "Canada")  # Exclude rows where Region is Canada
    ]                                                    #total = y is the total of all sub sectors
    co2eq_values = filtered_rows["CO2eq"].values
    #change datatype to float
    co2eq_values = [float(num) for num in co2eq_values]
    max_co2 = max(co2eq_values)
    #create a loop that iterates through co2 values, finds the associated "Region" and gets the 'lon' and 'lat' value from
    # the coordinates dataFrame and adds it as a new list into the heat map data list
    heatmap_data = []
    for index, row in filtered_rows.iterrows():
        region_name = row["Region"]

        # Find the corresponding coordinates for the region
        coord_row = data[data['name'] == region_name]

        if not coord_row.empty:  # Check if a matching region was found and parse it to a numeric value
            lat = float(coord_row['lat'].values[0])
            lon = float(coord_row['lon'].values[0])
            value = float(row["CO2eq"])/max_co2 #divide by the max value to get our opacity value between 0 and 1

            # Add CO2 value to the corresponding region in the DataFrame
            data.loc[data['name'] == region_name, 'co2_value'] = row["CO2eq"]

            # Add the data to heatmap_data
            heatmap_data.append([lat, lon, value])  # Append [latitude, longitude, CO2 value]

    HeatMap(heatmap_data, radius=50, blur=40, min_opacity=0.2).add_to(m)

#
# def generate_heatmap_over_time():
#     #load data
#     df = pd.read_csv("data/carbonemissions.csv")
#     #test source
#     source = "Buildings"
#     filtered_rows = df.loc[(df["Source"] == source)
#                        & (df["Total"] == "y")
#                        & (df["Region"] != "Canada")  # Exclude rows where Region is Canada
#     ]
#
#     # Get unique years and initialize list to store data for each year
#     years = sorted(filtered_rows["Year"].unique())
#     heatmap_data_by_year = []
#     #get max value of CO2
#     co2eq_values = filtered_rows["CO2eq"].values
#     #change datatype to float
#     co2eq_values = [float(num) for num in co2eq_values]
#     max_co2 = max(co2eq_values)
#
#     #loop through the years,
#     for year in years:
#         year_data = []
#         #refine the filtered rows to rows in the current year so we can loop over them
#         yearly_filtered_rows = filtered_rows[filtered_rows["Year"] == year]
#         #iterate through yearly rows
#         for _, row in yearly_filtered_rows.iterrows():
#             #get the region name
#             region = row["Region"]
#             #get the row from our province dataframe
#             region_row = data[data['name'] == region]
#             #get the lat and lon values from our dataframe
#             if not region_row.empty:
#                 lat = float(region_row['lat'].values[0])
#                 lon = float(region_row['lon'].values[0])
#                 # Ensure positive emission values
#                 emission = float(row["CO2eq"]) / max_co2 # Minimum opacity level to avoid issues
#                 #add the data to our year
#                 year_data.append([lat,lon,float(emission)])
#
#             # Add the year's data to the list
#         heatmap_data_by_year.append(year_data)
#
#     # Create and add the HeatMapWithTime layer
#     HeatMapWithTime(heatmap_data_by_year, radius=20, blur=20).add_to(m)
#
# #generate_heatmap_over_time()
#
# #generate markers

def generate_markers(data,m):
    with open('src/popup_template.html', 'r') as file:

        template = Template(file.read())

    for i in range(len(data)):
        co2_value_formatted = f"{float(data.iloc[i]['co2_value']):.2f}"
        # Render the template with data
        html = template.render(
            name=data.iloc[i]['name'],
            current_source=data.iloc[i]['current_source'],
            current_year=data.iloc[i]['current_year'],
            co2_value=co2_value_formatted
        )
        iframe = branca.element.IFrame(html=html, width=250, height=175)
        popup = folium.Popup(iframe, max_width=500) 
        folium.Marker(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=popup
        ).add_to(m)


if __name__ == "__main__":
    app.run(debug=True, port=9000)
