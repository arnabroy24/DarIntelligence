import xmltodict
import json

# Read XML file
with open("dark-web-info-batch-1.xml", "r") as xml_file:
    xml_data = xml_file.read()

# Parse XML to dictionary
xml_dict = xmltodict.parse(xml_data)

# Convert dictionary to JSON
json_data = json.dumps(xml_dict, indent=4)

# Print or write JSON
print(json_data)

# Optionally, write JSON to a file
with open("dweb1.json", "w") as json_file:
    json_file.write(json_data)