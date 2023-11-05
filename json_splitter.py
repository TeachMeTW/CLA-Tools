import json

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def find_unique_entries(json1, json2):
    unique = {}
    # Check for unique keys in json1
    for key, value in json1.items():
        if key not in json2:
            unique[key] = value
        elif value != json2[key]:
            unique[key] = value
    # Check for unique keys in json2
    for key, value in json2.items():
        if key not in json1:
            unique[key] = value
    return unique

# Paths to the JSON files
json_file_path1 = 'ds2.json'
json_file_path2 = 'ds3_filtered.json'
output_file_path = 'ds3max_filtered.json'

# Read the JSON files
json1 = read_json(json_file_path1)
json2 = read_json(json_file_path2)

# Find unique entries
unique_entries = find_unique_entries(json1, json2)

# Write the unique entries to a new JSON file
write_json(unique_entries, output_file_path)
