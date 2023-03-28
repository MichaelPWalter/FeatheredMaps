import pandas as pd
import os
import numpy as np


def ask_for_region_name():
    region_name=input("Region Name:  ")
    return region_name

def count_elevation(row,elevation_counts, min_elevation, max_elevation):
    elevation = row["elevation"]
    elevation = int(round(elevation / 10)* 10)
    # Increment the count of the current elevation in the dictionary
    if elevation in elevation_counts:
        elevation_counts[elevation] += 1
    else:
        elevation_counts[elevation] = 1
        # Update the overall minimum and maximum if necessary
        if elevation < min_elevation:
            min_elevation = elevation
        elif elevation > max_elevation:
            max_elevation = elevation
    
    return elevation_counts,min_elevation,max_elevation

def count_year(row,year_counts,min_year,max_year):
    year = row["year"]

    # Increment the count of the current year in the dictionary
    if year in year_counts:
        year_counts[year] += 1
    else:
        year_counts[year] = 1
        # Update the overall minimum and maximum if necessary
        if year < min_year:
            min_year = year
        elif year > max_year:
            max_year = year

    return year_counts,min_year,max_year

def count_month(row,month_counts):
    month = row["month"]

    # Increment the count of the current month in the dictionary
    if month in month_counts:
        month_counts[month] += 1
    else:
        month_counts[month] = 1
    
    return month_counts

def process_species(row,species_data):
    # Get the value in the "species" column
    species = row["species"]

    # Append the row to the DataFrame for this species
    if species not in species_data:
        species_data[species] = pd.DataFrame(columns=row.index)

    species_data[species] = pd.concat([species_data[species], row.to_frame().T], ignore_index=True)

    return species_data

def get_species_list(region_name):
    folder_path = f"Regions/{region_name}/species"
    folder_items = os.listdir(folder_path)

    # Filter the list to keep only folder names
    species_list = []
    for item in folder_items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            species_list.append(item)
    
    return species_list






# Set the chunk size to 100,000 lines
chunk_size = 10000

dtype = {
    'gbifID':np.int64,
    'species':str,
    'countryCode':str,
    'stateProvince':str,
    'individualCount':int,
    'decimalLatitude':float,
    'decimalLongitude':float,
    'elevation':int,
    'month':int,
    'year':int,
    'locality':str,
}

unique_species = 0
rows_processed = 0
elevation_counts = {}
min_elevation = int()
max_elevation = int()
year_counts = {} 
min_year = int()
max_year = int()
month_counts = {}

region_name= ask_for_region_name()

# Define the path to the CSV file
csv_file_path =f"Regions/{region_name}/{region_name}_elevation.csv"

# Iterate over the CSV file in chunks of 100,000 lines
for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size,dtype=dtype):
    species_data = {}

    #print(chunk["gbifID"].dtype)
    # Loop through the rows in the chunk
    for index, row in chunk.iterrows():

        elevation_counts,min_elevation,max_elevation = count_elevation(row,elevation_counts,min_elevation,max_elevation)
        year_counts,min_year,max_year = count_year(row,year_counts,min_year,max_year)
        month_counts = count_month(row,month_counts)

        species_data = process_species(row,species_data)

        rows_processed += 1


   # Save the DataFrames to CSV files for each species
    for species, data in species_data.items():
        #Create the species folder path
        species_folder_path = os.path.join(f"Regions/{region_name}/species/", species)
        header = False
        #Check if folder path already exists, if not we have a new species and we need to make the direcory and give the data a header
        if not os.path.exists(species_folder_path):
            os.makedirs(species_folder_path)
            header = True
            unique_species += 1
        species_csv_file_name = os.path.join(species_folder_path, f"{species}.csv")
        data.to_csv(species_csv_file_name, mode='a', header=header, index=False)
    

    
    print(f"Processed {rows_processed} and found {unique_species} unique species in the range of {min_elevation}m to {max_elevation}m", end= "\r")
 
species_list = get_species_list(region_name)


# Sample dictionary
my_dict = {"Region":[f"{region_name}"], 
           "entries":[rows_processed], 
           "unique Species":[unique_species], 
           "min_elevation":[min_elevation], 
           "max_elevation":[max_elevation],
           "min_year":[min_year],
           "max_year":[max_year],
           "species_list":[species_list],
           "month_count":[month_counts],
           "year_count":[year_counts],
           "elevation_count":[elevation_counts] 
           }

# Create a pandas DataFrame from the dictionary
df = pd.DataFrame(my_dict).T

# Save the DataFrame to a CSV file
summary_file_name = csv_file_path.split("elevation")[0] + "summary.csv"
df.to_csv(summary_file_name, header= False)

print("\nFinished processing")

