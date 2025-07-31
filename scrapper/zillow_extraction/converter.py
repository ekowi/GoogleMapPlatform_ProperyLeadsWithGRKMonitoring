
import csv
import json

input_csvs = ['output.csv', 'output_last.csv']
output_json = 'output_valid.json'
data = []

for input_csv in input_csvs:
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            latlong = row.get('latlong', '').strip()
            if latlong == '{}':
                continue
            data.append(row)

with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=2)