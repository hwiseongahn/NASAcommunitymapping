import json


def sort_by_year(json_file_path, output_file_path, yearWanted):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    data_for_this_year = []

    for entry in data:
        if entry["year"] == yearWanted:
            data_for_this_year.append(entry)

    with open(output_file_path, 'w') as file:
        json.dump(data_for_this_year, file, indent=4)


json_file_retrieve = "../res/co2_alberta_data.json"

#2019-2021
for year in range(2019, 2022):
    output_file_sent = f"../res/co2_{year}_data.json"
    sort_by_year(json_file_retrieve, output_file_sent, year)
