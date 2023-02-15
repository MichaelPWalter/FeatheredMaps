import pandas as pd


def standardize_IOC_taxonomy_csv(input_file):
    # Load the csv into a DataFrame and only include the specified columns
    df = pd.read_csv(input_file)
    
    
    df.insert(0, 'scientificName', df.pop('Species (Scientific)'))
    df.insert(1, 'IOC_common_name', df.pop('Common Name'))


    # Write the filtered DataFrame to a new csv
    df.to_csv(IOC_taxonomy_file.split("_cleaned")[0] + "_standardized.csv", index=False)


IOC_taxonomy_file = "Taxonomy/IOC/master_ioc_list_v13.1_cleaned.csv"

standardize_IOC_taxonomy_csv(IOC_taxonomy_file)

