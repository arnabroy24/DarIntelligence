import pandas as pd

# Read the XML file
df = pd.read_xml("dark-web-info-batch-1.xml")

# Print the DataFrame
print(df)