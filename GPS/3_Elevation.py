import pandas as pd
import requests
import time
import os
import shutil

def ask_for_region_name():
    region_name=input("Region Name:  ")
    return region_name

region_name= ask_for_region_name()

region_path = f"Regions/{region_name}/"

input_filename = region_path + f"{region_name}.csv"

temp_folder_path = region_path + "temp/"

missing_rows_filename = temp_folder_path + f"{region_name}_missing_rows.csv"

output_filename = input_filename.split(".csv")[0] + "_elevation.csv"



def pic_up_pieces(output_filename,input_filename,temp_folder_path,missing_rows_filename):
    if os.path.exists(output_filename):
        print("Picking up the pieces")
        os.makedirs(temp_folder_path)
        # Load the dataframes in chunks
        df1_chunks = pd.read_csv(input_filename, chunksize=10000,low_memory=False)
       # df2_chunks = pd.read_csv(output_filename, chunksize=10000,low_memory=False)

        number_missing_rows = 0
        # Find the missing rows
        for df1_chunk in df1_chunks:
            for df2_chunk in pd.read_csv(output_filename, chunksize=10000,low_memory=False):
                print_chunk = True
                # look for all values in missing_chunk['gbifID'] that are present in the df2_chunk and then only take the rows where this is not true (~True)
                if not df1_chunk.empty:
                    df1_chunk =df1_chunk[~df1_chunk['gbifID'].isin(df2_chunk['gbifID'])]
                    #print(len(df1_chunk))
                else:
                    print_chunk = False
                    break
            number_missing_rows += len(df1_chunk)
            print(f"chunk finished  found {number_missing_rows} rows so far", end= "\r")
            if print_chunk:
                df1_chunk.to_csv(missing_rows_filename, mode='a', header=not os.path.isfile(missing_rows_filename), index=False)
        print(f"Found {number_missing_rows} missing rows")
        

        
        input_filename_update = missing_rows_filename
        print(f"input file has been reassigned")
    else:
        input_filename_update = input_filename
    
    return input_filename_update


def check_for_completeness(region_name, output_filename):
    # Read in the first column of df1 and df2
    df1_col1 = pd.read_csv(f"Regions/{region_name}/{region_name}.csv", usecols=[0])
    df2_col1 = pd.read_csv(output_filename, usecols=[0])

    # Check if all values in df1_col1 are present in df2_col1
    all_values_present = df1_col1.iloc[:, 0].isin(df2_col1.iloc[:, 0]).all()

    if all_values_present:
        print("All values are present")
    else:
        print("There are values in the original .csv that are not present in the _elevation.csv.")

    return all_values_present

def remove_temp_folder (temp_folder_path):
    # remove the temporary folder and its contents
    try:
        shutil.rmtree(temp_folder_path)
    except:
        None

def save_chunk_to_csv(chunk,output_filename,i):
    # Save the updated chunk to a new CSV file
    header = False
    #Check if it is the first time the file has been created
    if i == 0:
        if not os.path.isfile(output_filename):
            #if so, we need a header
            header=True
    i += 1
    chunk.to_csv(output_filename, mode="a", index=False, header=header)
    return i

def API_call(locations):
    # Define the API endpoint and parameters
    url = "https://api.opentopodata.org/v1/aster30m"
    params = {
        "locations": locations,
        "interpolation": "cubic",
    }
    response = requests.post(url, data=params)
    results = response.json()["results"]
    return results

def update_csv(chunk,rows_without_elevation,results,number_of_locations_checked):
    #rows_without_elevation.drop(['decimalLatitude', 'decimalLongitude'], axis=1, inplace=True)
    elevations_list=[]
    for result in results:
        if result["elevation"] != None:
            elevations_list.append(result["elevation"])
        else:
            elevations_list.append(0)
    
    #remove the negative values and replace them with 0
    elevations_list = [max(0, x) for x in elevations_list]

    # Update the rows that don't have an elevation value with the retrieved elevations
    rows_without_elevation["elevation"] = elevations_list[:len(rows_without_elevation)]
    number_of_locations_checked += len(elevations_list)
    
    # Update the original "chunk" dataframe with the values from merged_df
    chunk.update(rows_without_elevation)
    #get rid of the floats
    chunk["elevation"] = chunk["elevation"].map(int)

    return chunk,number_of_locations_checked
                
def ETA(start_time,end_time,step_time_sum,i,number_of_locations_checked):
    step_time_sum += end_time - start_time
    step_time = step_time_sum/i
    try:
        percentage = round(number_of_locations_checked*100/total_amount_rows,1)
    except:
        percentage = "100"
    ETA_s = round((total_amount_rows-number_of_locations_checked)*step_time/100,0)
    ETA_seconds = int(ETA_s%60)
    ETA_minutes = ETA_s//60
    ETA_hours = int(ETA_minutes//60)
    ETA_minutes = int(ETA_minutes%60)
    print(f"Request Nr.{i}, total coordinates checked: {number_of_locations_checked}/{total_amount_rows} ({percentage} %)  ETA: {ETA_hours} h {ETA_minutes} min {ETA_seconds} s", end="\r")
    return step_time_sum

def process_chunk(input_filename,output_filename):
    # Read the input CSV file in chunks of 100 rows
    step_time_sum=0
    i,number_of_locations_checked = 0,0
    for chunk in pd.read_csv(input_filename, chunksize=100):
        start_time = time.time()
        
        #process the chunk by loading all rows that do not have an elevation value into a df
        rows_without_elevation = chunk[chunk["elevation"].isnull()][["gbifID", "decimalLatitude", "decimalLongitude", "elevation"]]
        if not rows_without_elevation.empty: 
            # load the locations from the df
            locations = "|".join([f"{lat},{lon}" for lat, lon in zip(rows_without_elevation["decimalLatitude"], rows_without_elevation["decimalLongitude"])])
            # Make API calls to get the elevations for the filtered rows
            results = API_call(locations)
            # Update the chunk with the elevation data
            chunk,number_of_locations_checked = update_csv(chunk,rows_without_elevation,results,number_of_locations_checked)
            i = save_chunk_to_csv(chunk,output_filename,i)
        # 1000 requests per day
        #request rate limit is 1/s
        time.sleep(1)
        end_time = time.time() 
        step_time_sum = ETA(start_time,end_time,step_time_sum,i,number_of_locations_checked)

    return number_of_locations_checked,i

def count_total_rows_without_elevation(input_filename):
    total_amount_rows = 0
    for chunk in pd.read_csv(input_filename, chunksize=100000, usecols=["elevation"]):
        rows_without_elevation = chunk[chunk["elevation"].isnull()]
        total_amount_rows += len(rows_without_elevation)
    return total_amount_rows



while True:
    # Sometimes the API call will fail for unknown reasons, that messes with the order
    
    try:
        #remove the temp folder from previous attemps
        remove_temp_folder(temp_folder_path)
        #check if there has been a previously aborted attempt
        input_filename_update = pic_up_pieces(output_filename,input_filename,temp_folder_path,missing_rows_filename)
        total_amount_rows = count_total_rows_without_elevation(input_filename_update)
        #Load the chunk, make the API call, update the chunk and save to csv
        number_of_locations_checked,i = process_chunk(input_filename_update,output_filename)
        check_for_completeness(region_name,output_filename)
        break

    except Exception as err:
        print("Something didnt work")
        print (err)
        if check_for_completeness(region_name,output_filename):
            remove_temp_folder(temp_folder_path)
            break
        else:
            time.sleep(60)


print(f"\nFinished checking {number_of_locations_checked} coordinated in {i} separate requests")




