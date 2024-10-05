import csv
import requests
import json
import pandas as pd

API_KEY = 'AIzaSyAkHIALksfdfAAz1cDH81OrY9_MKGTnuHM'


# Function to get city latitude and longitude using the Open-Meteo Geocoding API
def get_location_data(city_name):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&components=administrative_area:Alberta|country:CA&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]["geometry"]
            location = result["location"]
            print(location.get("lat"), location.get("lng"))
            return location.get("lat"), location.get("lng")
    return None, None


# Function to read city names from a CSV file and fetch location data
# def process_city_data(csv_file, output_json):
#     city_data = []
#
#     # Read data from the CSV file
#     df = pd.read_csv(csv_file)
#
#     for index, row in df.iterrows():
#         city_name = row['WaterbodyName']
#         year = "20" + str(row['CollectionYear'])
#         cellCount = row["CellCount"]
#         latitude, longitude = get_location_data(city_name)
#
#         # Create a dictionary with city information
#         city_info = {
#             "city_name": city_name,
#             "year": year,
#             "latitude": latitude,
#             "longitude": longitude,
#             "averageCellCount": cellCount
#         }
#         city_data.append(city_info)
#     print(city_data)
#     # Write the city data to a JSON file
#     with open(output_json, 'w') as json_file:
#         json.dump(city_data, json_file, indent=4)
#
#
# # Example usage
# csv_file = "dataCSV/albertaAlgaeRefined.csv"  # Input CSV file containing city names and emissions data
# output_json = "algae_city_data.json"  # Output JSON file to store city data

def process_city_data_for_CO2(csv_file, output_json):
    city_data = []

    # Read data from the CSV file
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        city_name = row['CSD']
        year = row['Period']
        co2_Value = row["OriginalValue"]
        latitude, longitude = get_location_data(city_name)

        # Create a dictionary with city information
        city_info = {
            "city_name": city_name,
            "year": year,
            "latitude": latitude,
            "longitude": longitude,
            "co2_Value": co2_Value
        }
        city_data.append(city_info)
    print(city_data)
    # Write the city data to a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(city_data, json_file, indent=4)


# Example usage
csv_file = "dataCSV/albertaCo2Refined.csv"  # Input CSV file containing city names and emissions data
output_json = "co2_alberta_data.json"  # Output JSON file to store city data

process_city_data_for_CO2(csv_file, output_json)
