""" import csv

# Open the CSV file
with open('temp/0091007-230224095556074.csv', encoding="utf-8", ) as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file, delimiter= "\t")
    # Read the first two lines
    line1 = next(csv_reader)
    line2 = next(csv_reader)
    # Display the lines
    print(line1)
    print(line2) """

""" 
a = 1356
b = 1351
c = 3.9

for i in [a,b,c]:
    print(f"{i} --> {int(round(i/10)*10)}")

 """

import pandas as pd

df = pd.read_csv("Regions\Galápagos\Galápagos_summary.csv",header=None,index_col=0).T
first_region = df.iloc[0]['month_count']
print(first_region.dtype)

#dfT = dfT.drop(df.columns[0],axis=1, inplace=True)
print(df)
