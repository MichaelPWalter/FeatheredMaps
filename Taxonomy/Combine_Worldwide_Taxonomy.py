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


# Write the filtered DataFrame to a new csv
merged_df.to_csv("Taxonomy/Combined_Worldwide_Taxonomy.csv", float_format="%.0f", index=False)


