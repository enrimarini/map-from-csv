import csv

# Define the input and output filenames
input_filename = 'input.csv'
output_filename = 'output.csv'

# Open the input file for reading
with open(input_filename, 'r') as input_file:
    # Create a CSV reader object
    reader = csv.DictReader(input_file)

    # Define the fieldnames for the output CSV
    fieldnames = ['date', 'time', 'location-long', 'location-lat']

    # Open the output file for writing
    with open(output_filename, 'w', newline='') as output_file:
        # Create a CSV writer object
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        # Write the header row to the output CSV
        writer.writeheader()

        # Loop over each row in the input CSV
        for row in reader:
            # Split the timestamp into separate date and time columns
            date, time = row['timestamp'].split(' ')

            # Write the updated row to the output CSV
            writer.writerow({
                'date': date,
                'time': time,
                'location-long': row['location-long'],
                'location-lat': row['location-lat']
            })

print('Data processing complete.')
