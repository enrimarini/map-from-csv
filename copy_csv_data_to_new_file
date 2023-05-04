import pandas as pd

# Set the name of the input CSV file
input_file = "input.csv"

# Set the names of the columns to extract
columns_to_extract = ["timestamp", "location-long", "location-lat"]

# Set the name of the output CSV file
output_file = "output.csv"

# Read in the input CSV file using pandas
data = pd.read_csv(input_file)

# Extract the desired columns
extracted_data = data[columns_to_extract]

# Write the extracted data to a new CSV file
extracted_data.to_csv(output_file, index=False)
