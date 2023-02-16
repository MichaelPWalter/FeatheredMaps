import pandas as pd
import os

# Find all files ending with "_standardized.csv" in all subdirectories
file_list = []
for root, dirs, files in os.walk(".", topdown=False):
    for file in files:
        if file.endswith("_standardized.csv"):
            file_path = os.path.join(root, file)
            file_list.append(file_path)

# Sort the list of file locations so that the file containing "IUCN" is first.
file_list = sorted(file_list, key=lambda x: "IUCN" not in x)


# Create an empty dataframe to store the merged data
merged_df = pd.DataFrame(columns=["scientificName"])

# Read each file into a dataframe and merge it with the previous data
for file in file_list:
    df = pd.read_csv(file)
    print(file)
    merged_df = merged_df.merge(df, on="scientificName", how="outer")

# Creating a new DataFrame with rows where IUCN_Species_Code is missing
Unmatched_df =merged_df[merged_df["IUCN_Species_Code"].isna()].copy()
#Unmatched_df = Unmatched_df.drop(columns=[["IUCN_Species_Code"],["IUCN_common_name"],["altcommonNames"],["Synonym"]])

# Removing rows where IUCN_Species_Code is missing from original_df
merged_df.dropna(subset=["IUCN_Species_Code"], inplace=True)





# Iterate over all rows in Unmatched_df
for _, row in Unmatched_df.iterrows():
    # Iterate over all columns that contain "_common_name" but not "IUCN_common_name"
    for col in [c for c in merged_df.columns if '_common_name' in c and c != 'IUCN_common_name']:
        # Check for matches between scientificName and Synonym and copy matching common names
        mask = merged_df['Synonym'].str.contains(row['scientificName'], na=False)
        if mask.any():
            merged_df.loc[mask, col] = row[col]

    # Only append row if no matches were found
    if not mask.any():
        merged_df = merged_df.append(row, ignore_index=True)


#synonyms_df.to_csv("Taxonomy/Combined_Worldwide_Taxonomy_Synonyms.csv", float_format="%.0f", index=False)
# Write the filtered DataFrame to a new csv
merged_df.to_csv("Taxonomy/Combined_Worldwide_Taxonomy.csv", float_format="%.0f", index=False)



