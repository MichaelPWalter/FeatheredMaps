import pandas as pd
import rasterio

# Define the path to the SRTM elevation file
elevation_file = 'GPS\Galápagos.csv'

# Define a function to compute the elevation value for a given (latitude, longitude) pair
def compute_elevation(latitude, longitude):
    with rasterio.open(elevation_file) as src:
        x, y = src.index(longitude, latitude)
        return int(src.read(1)[y, x])

# Open the input CSV file as a pandas DataFrame
df = pd.read_csv('path/to/input_file.csv')

# Create a new column in the DataFrame to store the elevation values
df['elevation'] = pd.Series(dtype=int)

# Iterate over the rows of the DataFrame and compute the elevation value for each row
for index, row in df.iterrows():
    elevation = compute_elevation(row['Latitude'], row['Longitude'])
    df.at[index, 'elevation'] = elevation

# Save the updated DataFrame to a new CSV file
df.to_csv('GPS\Galápagos_elevation.csv', index=False)