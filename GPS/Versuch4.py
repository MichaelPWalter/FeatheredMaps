import pandas as pd
import zipfile

# path to your large zipped csv file
zip_path = 'GPS/occurrences.zip'

# name of the csv file inside the zip file
csv_filename = '0100400-230224095556074.csv'

# select the columns you are interested in
columns_of_interest = ['gbifID', 'species', 'decimalLatitude', 'decimalLongitude', 'elevation', 'day', 'month', 'year', 'countryCode', 'stateProvince', 'locality','coordinateUncertaintyInMeters','occurrenceStatus','individualCount']

# define the filter criteria
def filter_func(df):
    #print("here")
    return ((df['species'].notnull()) 
            & ((df['coordinateUncertaintyInMeters'].isnull()) | (df['coordinateUncertaintyInMeters'] <= 2000))
            & (df['occurrenceStatus'] == 'PRESENT') 
            & (df['month'].notnull()))

# define the locality split function
def split_func(locality):
    # use a regular expression to match only those "--" occurrences that are preceded or followed by a letter
    split_df = locality.str.extract(r'^(?P<locality_1>[A-Za-z].*?[A-Za-z])?(?:--)(?P<locality_2>[A-Za-z].*?[A-Za-z])?$', expand=True)
    split_df['locality_1'] = split_df['locality_1'].str.strip()
    split_df['locality_2'] = split_df['locality_2'].str.strip()
    # check if no split occurred
    if split_df['locality_1'].isna().all() and split_df['locality_2'].isna().all():
        split_df['locality_1'] = locality.copy()
    elif split_df['locality_2'].isna().any():
        # assume the first part of the split is in locality_1
        split_df['locality_1'].fillna(locality, inplace=True)
    return split_df

if input("Have you extracted the file yet ? y/n:  ").lower() != "y":
    print("extracting {csv_filename} ...")
    # extract the zipped csv file to a temporary folder
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extract(csv_filename, path='temp')
    print("finished extraction")


# process the data in chunks
chunk_size = 10000
#filtered_headers = pd.DataFrame(columns=columns_of_interest)
i = 0   

# Iterate over the csv file in chunks and filter the data
for chunk in pd.read_csv('temp/' + csv_filename, delimiter='\t', usecols=columns_of_interest, chunksize=chunk_size, low_memory=False):
    chunk["individualCount"].fillna(1, inplace=True)
    chunk["individualCount"] = chunk["individualCount"].astype(int)
    chunk["locality"] = chunk["locality"].map(str)
    filtered_chunk = chunk[filter_func(chunk)]
    split_locality = split_func(filtered_chunk['locality'])

    filtered_chunk = pd.concat([filtered_chunk, split_locality], axis=1)
    filtered_chunk.drop(['coordinateUncertaintyInMeters', 'locality', 'occurrenceStatus'], axis=1, inplace=True)
    if i == 0:
        filtered_chunk.to_csv('SoussMassa.csv', index=False, mode='w', header=True)
        i += 1
    else:
        filtered_chunk.to_csv('SoussMassa.csv', index=False, mode='a', header=False)
    
    # Clear the filtered_data dataframe
    filtered_chunk = pd.DataFrame(columns=columns_of_interest)

# remove the temporary folder and its contents
import shutil
shutil.rmtree('temp')