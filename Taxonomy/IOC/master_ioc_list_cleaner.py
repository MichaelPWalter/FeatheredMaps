import pandas as pd

def clean_master_ioc_list_xlsx(input_file, output_file):

    """ 
    The function clean_master_ioc_list_xlsx takes two arguments, 
    input_file and output_file, which are the paths to an Excel file 
    and the desired output file, respectively. 
    
    The function performs the following operations on the data in the input file:
    - Loads the columns "Genus", "Species (Scientific)", and "Species (English)" from the input file into a Pandas DataFrame.
    - Fills in any empty cells in the "Genus" column with the value from the cell above it.
    - Removes any rows in the DataFrame where the "Species (Scientific)" column is empty.
    - Combines the values in the "Genus" and "Species (Scientific)" columns into a new "Species (Scientific)" column. The "Genus" column is then dropped.
    - Renames the "Species (English)" column to "Common Name".
    - Writes the processed DataFrame to a new CSV file specified by output_file.
    """

    # Load the specified columns from the xlsx file into a DataFrame
    df = pd.read_excel(input_file, usecols=["Genus", "Species (Scientific)", "Species (English)"], header=3)

    # Fill in any empty cells in column "Genus" with the value above
    df['Genus'] = df['Genus'].ffill()

    # Remove any rows where column "Species (Scientific)" is empty
    df = df.dropna(subset=['Species (Scientific)'])

    # Combine columns "Genus" and "Species (Scientific)" into a new column "Species (Scientific)"
    df['Species (Scientific)'] = df['Genus'].astype(str) + ' ' + df['Species (Scientific)'].astype(str)
    df = df.drop(['Genus'], axis=1)

    # Rename column "Species (English)" to "Common Name"
    df = df.rename(columns={'Species (English)': 'Common Name'})

    # Write the processed DataFrame to a new xlsx file
    df.to_csv(output_file, index=False)


IOC_taxonomy_file = "IOC_World_Bird_List/master_ioc_list_v13.1.xlsx"

clean_master_ioc_list_xlsx(IOC_taxonomy_file,IOC_taxonomy_file.split(".xlsx")[0] + "_cleaned.csv")
