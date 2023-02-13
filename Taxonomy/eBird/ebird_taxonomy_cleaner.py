import pandas as pd

def clean_eBird_taxonomy_csv(input_file, output_file):

    """
    This function takes two arguments: 
    input_file which is the path to the input CSV file, 
    and output_file which is the path to the output CSV file. 

    The function will produce a new csv file named output_file 
    that only contains the columns "CATEGORY","SPECIES_CODE","PRIMARY-COM-NAME" and "SCI_NAME" 
    and only the rows where "CATEGORY" is equal to "species". 

    To use this function, you would call it as follows:

    clean_eBird_taxonomy_csv('your_file.csv', 'filtered_file.csv') 
    """

    # Load the csv into a DataFrame and only include the specified columns
    df = pd.read_csv(input_file, usecols=["CATEGORY","SPECIES_CODE","PRIMARY_COM_NAME","SCI_NAME"])

    # Filter the DataFrame to only keep rows where "CATEGORY" is equal to "species"
    df = df[df['CATEGORY'] == 'species']

    # Write the filtered DataFrame to a new csv
    df.to_csv(output_file, index=False)

eBird_taxonomy_file = "eBird_Taxonomy/ebird_taxonomy_v2022.csv"

clean_eBird_taxonomy_csv(eBird_taxonomy_file,eBird_taxonomy_file.split(".csv")[0] + "_cleaned.csv")
