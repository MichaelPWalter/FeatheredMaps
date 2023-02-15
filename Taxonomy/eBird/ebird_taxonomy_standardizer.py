import pandas as pd


def standardize_eBird_taxonomy_csv(input_file):
    # Load the csv into a DataFrame and only include the specified columns
    df = pd.read_csv(input_file)
    
    
    df.insert(0, 'scientificName', df.pop('SCI_NAME'))
    df.insert(1, 'eBird_Species_Code', df.pop('SPECIES_CODE'))
    df.insert(2, 'eBird_common_name', df.pop('PRIMARY_COM_NAME'))

    # Write the filtered DataFrame to a new csv
    df.to_csv(eBird_taxonomy_file.split("_cleaned")[0] + "_standardized.csv", index=False)


eBird_taxonomy_file = "Taxonomy/eBird/ebird_taxonomy_v2022_cleaned.csv"

standardize_eBird_taxonomy_csv(eBird_taxonomy_file)




