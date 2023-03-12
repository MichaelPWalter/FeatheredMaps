import pandas as pd
import zipfile

# path to your large zipped csv file
zip_path = 'occurrences.zip'

# name of the csv file inside the zip file
csv_filename = '0079863-230224095556074.csv'

# select the columns you are interested in
columns_of_interest = ['gbifID', 'species', 'decimalLatitude', 'decimalLongitude', 'elevation', 'day', 'month', 'year', 'countryCode', 'stateProvince', 'locality','coordinateUncertaintyInMeters','occurrenceStatus']

# define the filter criteria
def filter_func(df):
    return ((df['species'].notnull()) 
            & ((df['coordinateUncertaintyInMeters'].isnull()) | (df['coordinateUncertaintyInMeters'] <= 1000))
            & (df['occurrenceStatus'] == 'PRESENT') 
            & (df['month'].notnull()))

# define the locality split function
def split_func(locality):
    # use a regular expression to match only those "--" occurrences that are preceded or followed by a letter
    split_df = locality.str.extract(r'^(?P<locality_1>[A-Za-z].*?[A-Za-z])?(?:--)(?P<locality_2>[A-Za-z].*?[A-Za-z])?$', expand=True)
    split_df['locality_1'] = split_df['locality_1'].str.strip()
    split_df['locality_2'] = split_df['locality_2'].str.strip()
    # check if no split occurred
    if split_df['locality_1'].isna().any():
        split_df['locality_1'] = locality.copy()
    return split_df

# extract the zipped csv file to a temporary folder
with zipfile.ZipFile(zip_path, 'r') as zip_file:
    zip_file.extract(csv_filename, path='temp')

# process the data in chunks
chunk_size = 10000
filtered_data = pd.DataFrame(columns=columns_of_interest)

for chunk in pd.read_csv('temp/' + csv_filename,
                         delimiter='\t',
                         usecols=columns_of_interest,
                         chunksize=chunk_size,
                         low_memory=False):
    chunk = chunk[filter_func(chunk)]
    split_locality = split_func(chunk['locality'])
    chunk = pd.concat([chunk, split_locality], axis=1)
    filtered_data = pd.concat([filtered_data, chunk], ignore_index=True)

# save the filtered data to a new csv file
filtered_data = filtered_data.drop(['coordinateUncertaintyInMeters', 'locality', 'occurrenceStatus'], axis=1)
filtered_data.to_csv('filtered_data.csv', index=False)

# remove the temporary folder and its contents
import shutil
shutil.rmtree('temp')