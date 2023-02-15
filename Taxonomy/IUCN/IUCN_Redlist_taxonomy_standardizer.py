import pandas as pd


def standardize_IUCN_taxonomy_csv(input_file):
    # Load the csv into a DataFrame and only include the specified columns
    df = pd.read_csv(input_file)
    
    
    df.insert(0, 'scientificName', df.pop('scientificName'))
    df.insert(1, 'IUCN_Species_Code', df.pop('internalTaxonId'))
    df.insert(2, 'IUCN_common_name', df.pop('maincommonName'))

    # Write the filtered DataFrame to a new csv
    df.to_csv(IUCN_taxonomy_file.split("_cleaned")[0] + "_standardized.csv", index=False)


IUCN_taxonomy_file = "Taxonomy\IUCN\IUCN_Redlist_taxonomy_cleaned.csv"

standardize_IUCN_taxonomy_csv(IUCN_taxonomy_file)

