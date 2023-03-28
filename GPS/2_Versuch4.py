import pandas as pd
import zipfile
import os
import numpy as np

def ask_for_region_name():
    region_name=input("Region Name:  ")
    return region_name

region_name= ask_for_region_name()

# path to your large zipped csv file
zip_path = f'Regions/{region_name}/{region_name}.zip'

# name of the csv file inside the zip file
#csv_filename = '0101895-230224095556074.csv'

#name of the output file
output_filename = f'Regions/{region_name}/{region_name}.csv'


def filter_func(df):
    #print("here")
    return ((df['species'].notnull()) 
            & ((df['coordinateUncertaintyInMeters'].isnull()) | (df['coordinateUncertaintyInMeters'] <= 2000))
            & (df['occurrenceStatus'] == 'PRESENT') 
            & (df['month'] > 0))


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


def unzip(zip_path):
    print(f"extracting {zip_path} ...")
    # extract the zipped csv file to a temporary folder
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(path='temp')
    print("finished extraction")


def filter():
    csv_filename = os.listdir("temp")[0]
    # process the data in chunks
    chunk_size = 10000
    #filtered_headers = pd.DataFrame(columns=columns_of_interest)
    i = 0   
    # select the columns you are interested in
    columns_of_interest = ['gbifID', 'species', 'decimalLatitude', 'decimalLongitude', 'elevation', 'month', 'year', 'countryCode', 'stateProvince', 'locality','coordinateUncertaintyInMeters','occurrenceStatus','individualCount']

    dtype = {
        'gbifID':np.int64,
        'species':str,
        'countryCode':str,
        #'stateProvince':str,
        #'individualCount':int, has NaN
        'decimalLatitude':float,
        'decimalLongitude':float,
        #'elevation':int,
        #'month':int,
        'year':int,
        #'locality':str
    }


    # Iterate over the csv file in chunks and filter the data
    for chunk in pd.read_csv('temp/' + csv_filename, delimiter='\t', usecols=columns_of_interest, chunksize=chunk_size, dtype=dtype, low_memory=False):
        chunk["stateProvince"].fillna("", inplace = True)
        chunk["stateProvince"] = chunk["stateProvince"].astype(str)
        chunk["individualCount"].fillna(1, inplace=True)
        chunk["individualCount"] = chunk["individualCount"].astype(int)
        chunk["locality"].fillna("", inplace=True)
        chunk["locality"] = chunk["locality"].map(str)
        chunk["month"].fillna(0, inplace= True)
        chunk["month"] = chunk["month"].astype(int)
        #print(chunk)
        filtered_chunk = chunk[filter_func(chunk)]
        #print(filtered_chunk)
        #split_locality = split_func(filtered_chunk['locality'])

        #filtered_chunk = pd.concat([filtered_chunk, split_locality], axis=1)
        finished_chunk = filtered_chunk.drop(['coordinateUncertaintyInMeters','occurrenceStatus'], axis=1)
        
        if i == 0:
            finished_chunk.to_csv(output_filename, index=False, mode='a', header=True)
            i += 1
        else:
            finished_chunk.to_csv(output_filename, index=False, mode='a', header=False)
        
        # Clear the filtered_data dataframe
        filtered_chunk = pd.DataFrame(columns=columns_of_interest)
        finished_chunk = pd.DataFrame(columns=columns_of_interest)

    # remove the temporary folder and its contents
    import shutil
    shutil.rmtree('temp')

unzip(zip_path=zip_path)

filter()