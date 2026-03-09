import json
data = []

with open('tools/ProcessedList.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if ":" in line:
            id_part, name_part = line.split(":", 1)
            id = int(id_part.strip())
            name = name_part.strip()
            data.append({"id": id, "name": name})

# Write to JSON file
with open('imageCategories/OIv7/Stackable.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)