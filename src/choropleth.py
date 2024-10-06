import folium
import pandas as pd
import json
from folium import Choropleth, LayerControl
from branca.element import Template, MacroElement

def generate_choropleth(source, year,data,m):
    df = pd.read_csv("res/carbonemissions.csv")

    data['current_year'] = year #set the year so we can access it for the marker
    data['current_source'] = source #set the source so we can access it for the marker
    
    filtered_rows = df.loc[
        (df["Source"] == source) &
        (df["Year"] == year) &
        (df["Total"] == "y") &
        (df["Region"] != "Canada")
    ].copy()

    combined_region_rows = filtered_rows[filtered_rows['Region'] == 'Northwest Territories and Nunavut']
    # combined row fro the certain years, like 1990 till 1991 ish?
    duplicate_rows_nt = combined_region_rows.copy()
    duplicate_rows_nt['Region'] = 'Northwest Territories'
    duplicate_rows_nu = combined_region_rows.copy()
    duplicate_rows_nu['Region'] = 'Nunavut'

    # rmoving those iterations to make it easier to handle for the merge 
    filtered_rows = filtered_rows[filtered_rows['Region'] != 'Northwest Territories and Nunavut']
    filtered_rows = pd.concat([filtered_rows, duplicate_rows_nt, duplicate_rows_nu], ignore_index=True)

    name_mapping = {
        'Newfoundland & Labrador': 'Newfoundland and Labrador',
        'PEI': 'Prince Edward Island',
        'Nova-Scotia': 'Nova Scotia',
        'NWT': 'Northwest Territories',
        'Nunavut (NU)': 'Nunavut',
        'NU': 'Nunavut',
    } # mapping for the 
    filtered_rows['Region'] = filtered_rows['Region'].replace(name_mapping)

    # numeric error check from heatmap
    filtered_rows['CO2eq'] = pd.to_numeric(filtered_rows['CO2eq'], errors='coerce')

    filtered_rows['CO2eq'].fillna(0, inplace=True)

    # read the GeoJSON data containing Nunavut and NWT
    geojson_file_path = 'res/georef-canada-province@publicTEST.geojson'

    with open(geojson_file_path, 'r') as f:
        geojson_data = json.load(f)

    for feature in geojson_data['features']:
        if 'prov_name_en' in feature['properties']:
            if isinstance(feature['properties']['prov_name_en'], list):
                feature['properties']['prov_name_en'] = feature['properties']['prov_name_en'][0]
        else:
            print("Warning: 'prov_name_en' not found in feature properties.")

    dataframe_provinces = filtered_rows['Region'].unique()
    print("\nProvince names properly updated based off geoJSON file:")
    print(dataframe_provinces)

    #  added check to make sure it's lining up properly wihtout errors, converting them into a unified namespace 
    geojson_provinces = [feature['properties']['prov_name_en'] for feature in geojson_data['features']]
    print("\nProvince names in GeoJSON:")
    print(geojson_provinces)

    #m = folium.Map(location=[56.130, -106.35], zoom_start=4, tiles="cartodb positron")
    # map call staying in function same as heatmap

    choropleth = Choropleth(
        geo_data=geojson_data,
        data=filtered_rows,
        columns=['Region', 'CO2eq'],
        key_on='feature.properties.prov_name_en',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='CO2 Emissions (kt CO2eq)',
        # makes sure unit matches up 
        smooth_factor=0
    ).add_to(m)

    LayerControl().add_to(m)

    legend_html = '''
    {% macro html(this, kwargs) %}
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; width: 150px; height: 90px; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:white;
        ">
        &nbsp;<b>CO2 Emissions</b><br>
        &nbsp;High &nbsp;<i class="fa fa-square" style="color:#800026"></i><br>
        &nbsp;Medium &nbsp;<i class="fa fa-square" style="color:#FC4E2A"></i><br>
        &nbsp;Low &nbsp;<i class="fa fa-square" style="color:#FFEDA0"></i>
    </div>
    {% endmacro %}
    '''
    macro = MacroElement()
    macro._template = Template(legend_html)
    m.get_root().add_child(macro)

    #m.save("TEST_Choropleth.html")

