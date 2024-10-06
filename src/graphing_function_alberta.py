import matplotlib.pyplot as plt
import json


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def plot_data_by_year_ALGAE(data_by_year, year):
    city_name = []
    cellCount = []

    for city in data_by_year:
        city_name.append(city["city_name"])
        cellCount.append(city["averageCellCount"])

    plt.figure(figsize=(20, 12))

    plt.bar(city_name, cellCount, color='green')

    plt.title(f'Alberta in {year}', fontsize=16, fontweight= 'bold')
    plt.xlabel('City Name in Alberta', fontsize=14, fontweight= 'bold' )
    plt.ylabel('Cell Count (cells/mL)', fontsize=14, fontweight= 'bold')

    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yscale('log')

    plt.tight_layout()

    plt.savefig(f'../graphs/algae/algae_graph_{year}.png')


def plot_data_by_year_CO2(data_by_year, year):
    city_name = []
    co2_value = []

    for city in data_by_year:
        city_name.append(city["city_name"])
        co2_value.append(city["co2_Value"])

    plt.figure(figsize=(35, 16))

    plt.bar(city_name, co2_value, color='red')

    plt.title(f'Alberta in {year}', fontsize=16, fontweight= 'bold')
    plt.xlabel('City Name in Alberta', fontsize=14, fontweight= 'bold' )
    plt.ylabel('CO2 Emission Value (tonnes of gas)', fontsize=14, fontweight= 'bold')

    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yscale('log')

    plt.tight_layout()

    plt.savefig(f'../graphs/CO2/co2_graph_{year}.png')


for year in range(2019, 2022):
    plot_data_by_year_CO2(load_json_data(f"../res/co2_{year}_data.json"), year)
    plot_data_by_year_ALGAE(load_json_data(f"../res/algae_{year}_data.json"), year)