import pandas as pd
import zipfile as zip
import shutil
import numpy as np



path_to_zip_file = "Taxonomy/IUCN/redlist_species_data_2023_02_05.zip"
unzipped_dir = "Taxonomy/IUCN/redlist_species_data_2023_02_05/"
common_names_csv = "Taxonomy/IUCN/redlist_species_data_2023_02_05/common_names.csv"
synonyms_csv = "Taxonomy/IUCN/redlist_species_data_2023_02_05/synonyms.csv"
assessment_csv = "Taxonomy/IUCN/redlist_species_data_2023_02_05/assessments.csv"
cleaned_csv = "Taxonomy/IUCN/IUCN_Redlist_taxonomy_cleaned.csv"
cleaned_and_vulnerability_csv = "Taxonomy/IUCN/IUCN_Redlist_taxonomy_cleaned_and_vulnerability.csv"


def remove_other_languages(DataFrame):
    # Filter the rows where the "language" column is equal to "English"
    DataFrame = DataFrame[DataFrame["language"] == "English"]

    DataFrame = DataFrame.copy()
    # Drop the "language" column
    DataFrame.drop("language", axis=1, inplace=True)

    return DataFrame

def sort_by_scientificName(DataFrame):
    # Sort the DataFrame in ascending order by the "scientificName" column
    DataFrame.sort_values("scientificName", inplace=True, ascending=True)

    return DataFrame


def group_commonNames(DataFrame):
    # Group the data frame by "scientificName" and aggregate the "name" column using the lambda function to join all values
    # into a comma-separated string. For the "internalTaxonId" column, keep the first value for each group. Finally, reset the index.
    DataFrame = DataFrame.groupby("scientificName").agg({'name': lambda x: ', '.join(x),'internalTaxonId': 'first'}).reset_index()

    return DataFrame

def get_main_commonName(DataFrame):
    # Split the "altcommonNames" column by comma
    DataFrame['name'] = DataFrame['name'].str.split(', ')

    # Extract the last entry of the split list and add it to a new column called "maincommonName"
    DataFrame['maincommonName'] = DataFrame['name'].str.get(-1)

    # Remove the last entry from the "altcommonNames" list
    DataFrame['name'] = DataFrame['name'].apply(lambda x: x[:-1]).apply(', '.join)


    DataFrame.rename(columns={'name': 'altcommonNames'}, inplace=True)

    return DataFrame

def clean_synonym_csv(DataFrame):

    # Select only the columns "scientificName", "genusName", and "speciesName"
    DataFrame = DataFrame[["scientificName", "genusName", "speciesName"]]

    # Replace empty values in the "speciesName" column with a blank string
    DataFrame["speciesName"].fillna("", inplace=True)

    # Concatenate the "genusName" and "speciesName" columns with a space as separator
    DataFrame["Synonym"] = DataFrame["genusName"] + " " + DataFrame["speciesName"]

    # If "speciesName" is empty, use only the "genusName" value
    DataFrame["Synonym"] = DataFrame["Synonym"].where(DataFrame["speciesName"] != "", DataFrame["genusName"])

    # Drop the original "genusName" and "speciesName" columns
    DataFrame = DataFrame.drop(["genusName", "speciesName"], axis=1)

    # Remove duplicates from the dataframe and keep only the first occurrence
    DataFrame = DataFrame.drop_duplicates(keep='first')
    
    return DataFrame

def group_synonyms(DataFrame):
    # Group the data frame by "scientificName" and aggregate the "name" column using the lambda function to join all values
    # into a comma-separated string. For the "internalTaxonId" column, keep the first value for each group. Finally, reset the index.
    DataFrame = DataFrame.groupby("scientificName").agg({'Synonym': lambda x: ', '.join(x)}).reset_index()

    return DataFrame

def merge_df_and_synonyms(df,syn):
    # Merge the two DataFrames on the "scientificName" column using a left join
    df = pd.merge(df, syn, on='scientificName', how='outer')

    return df

def remove_duplicates(df):
    for idx, row in df.iterrows():
        common_name = row['maincommonName']
        alt_names = row['altcommonNames']
        if isinstance(alt_names, str):
            alt_names = [name.strip() for name in alt_names.split(",") if name.strip() != common_name]
            #alt_names = list(set(alt_names))
            if len(alt_names) == 0:
                alt_names = np.nan
            else:
                # join list to create comma-separated string
                alt_names = ", ".join(alt_names)
            df.at[idx, 'altcommonNames'] = alt_names
        else:
            df.at[idx, 'altcommonNames'] = np.nan

    return df


def merge_df_and_vul(df,vul):
    # Merge the two DataFrames on the "internalTaxonId" column using a left join
    df = pd.merge(df, vul, on='internalTaxonId', how='left')
    df["assessmentDate"] = pd.to_datetime(df["assessmentDate"]).dt.strftime("%Y")

    return df


#unzip the zip file into an equally names folder
try:
    with zip.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(unzipped_dir)
    Created_temp_folder = True
except:
    print(Exception)

# Read the input csv file into a pandas DataFrame

df = pd.read_csv(common_names_csv)

df = remove_other_languages(df)

#df = sort_by_scientificName(df)

df = group_commonNames(df)

df = get_main_commonName(df)

syn = pd.read_csv(synonyms_csv)

syn_cleaned = clean_synonym_csv(syn)

syn_cleaned = group_synonyms(syn_cleaned)

df = merge_df_and_synonyms(df,syn_cleaned)

df = remove_duplicates(df)

# Save the new dataframe to a new CSV file
df.to_csv(cleaned_csv, index=False)

vul = pd.read_csv(assessment_csv, usecols=["internalTaxonId","redlistCategory","assessmentDate" ,"populationTrend","yearLastSeen"])

df = merge_df_and_vul(df,vul)

if Created_temp_folder == True:
    shutil.rmtree(unzipped_dir)

# Insert the "maincommonName" column at position 2 and the "altcommonNames" column at position 3
df.insert(0, 'internalTaxonId', df.pop('internalTaxonId'))
df.insert(1, 'scientificName', df.pop('scientificName'))
df.insert(2, 'Synonym', df.pop('Synonym'))
df.insert(3, 'maincommonName', df.pop('maincommonName'))
df.insert(4, 'altcommonNames', df.pop('altcommonNames'))
df.insert(5, 'redlistCategory', df.pop('redlistCategory'))
df.insert(6, 'assessmentDate', df.pop('assessmentDate'))
df.insert(7, 'populationTrend', df.pop('populationTrend'))
df.insert(8, 'yearLastSeen', df.pop('yearLastSeen'))


# Save the filtered and modified DataFrame to a new csv file.
df.to_csv(cleaned_and_vulnerability_csv, index=False)

print(df.loc[df["scientificName"]=="Accipiter imitator"])

