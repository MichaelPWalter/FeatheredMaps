import matplotlib.pyplot as plt
import math
import pandas as pd
import ast

def ask_for_region_name():
    region_name=input("Region Name:  ")
    return region_name

def csv_to_dict(csv_file_name):

    df = pd.read_csv(csv_file_name,header=None,index_col=0).T

    elevation_count = ast.literal_eval(df.iloc[0]['elevation_count'])
    year_count = ast.literal_eval(df.iloc[0]['year_count'])
    month_count = ast.literal_eval(df.iloc[0]['month_count'])
    min_elevation = int(df.iloc[0]['min_elevation'])
    max_elevation = int(df.iloc[0]['max_elevation'])
    #elevation_count = re.sub(r'(\w+):', r'"\1":', elevation_count)
    #elevation_count = json.loads(elevation_count)
    
    #year_count = df.iloc[0]['year_count']
    #year_count = re.sub(r'(\w+):', r'"\1":', year_count)
    #year_count = json.loads(year_count)

    #month_count = df.iloc[0]['month_count']
    #month_count = re.sub(r'(\w+):', r'"\1":', month_count)
    #month_count = json.loads(month_count)
 
    return elevation_count,year_count,month_count,min_elevation,max_elevation


region_name = ask_for_region_name()

csv_file_name = f"Regions/{region_name}/{region_name}_summary.csv"

elevation_count,year_count,month_count,min_elevation,max_elevation = csv_to_dict(csv_file_name)

# Input data
x = list(elevation_count.values())
x = [int(round(i/50)*50)+1 for i in x]
x = [math.log(i) for i in x]
y = list(elevation_count.keys())

height = (max_elevation-min_elevation)/20

plt.barh(y, x, height=height, color="green")
plt.style.use('seaborn')

# get the axis object
ax = plt.gca()

# remove the spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


plt.xlabel('Count')
plt.ylabel('Elevation')
plt.show()

# Input data
y = list(year_count.values())
x = list(year_count.keys())

plt.bar(x, y, width=0.8, edgecolor='black', color="green")
plt.style.use('seaborn')

# get the axis object
ax = plt.gca()

# remove the spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.xlabel('Year')
plt.ylabel('Count')
plt.show()

# Input data
x = list(month_count.values())
y = list(month_count.keys())

plt.bar(y, x, width=0.8, edgecolor='black', color="green")
plt.style.use('seaborn')

# get the axis object
ax = plt.gca()

# remove the spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


plt.xlabel('Count')
plt.ylabel('Month')
plt.show()


""" 
import matplotlib.pyplot as plt

# Define data for the first plot
x1 = [10, 0, 130, 450, 1000]
y1 = [101576, 99792, 6975, 4689, 574]

# Define data for the second plot
x2 = [20, 0, 260, 900, 2000]
y2 = [123456, 87654, 4321, 9876, 456]

# Define data for the third plot
x3 = [30, 0, 390, 1350, 3000]
y3 = [654321, 34567, 8765, 1234, 987]

# Set the style and color
plt.style.use('ggplot')
color = '#B2D8D8'

# Create the subplots
fig, axs = plt.subplots(3, 1, figsize=(6, 10))

# Plot the first graph
axs[0].barh(x1, y1, height=1, color=color)
axs[0].set_xlim(0, max(y1)*1.1)
axs[0].set_xlabel('Count')
axs[0].set_ylabel('Elevation (m)')
axs[0].set_title('Elevation Count')

# Plot the second graph
axs[1].barh(x2, y2, height=1, color=color)
axs[1].set_xlim(0, max(y2)*1.1)
axs[1].set_xlabel('Count')
axs[1].set_ylabel('Elevation (m)')
axs[1].set_title('Elevation Count')

# Plot the third graph
axs[2].barh(x3, y3, height=1, color=color)
axs[2].set_xlim(0, max(y3)*1.1)
axs[2].set_xlabel('Count')
axs[2].set_ylabel('Elevation (m)')
axs[2].set_title('Elevation Count')

# Adjust the spacing between the subplots
plt.subplots_adjust(hspace=0.5)

# Display the plot
plt.show() """