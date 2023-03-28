import matplotlib.pyplot as plt
import math

# Input data
elevation_count = {10: 101576, 0: 99792, 130: 6975, 450: 4689, 1000: 574, 40: 3910, 120: 1066, 610: 12780, 240: 355, 50: 2677, 20: 32720, 360: 172, 150: 285, 600: 873, 930: 16, 920: 94, 790: 19, 60: 6353, 400: 5012, 380: 2809, 270: 186, 30: 4014, 210: 332, 910: 3909, 80: 1234, 230: 4556, 1020: 1435, 140: 148, 160: 610, 410: 270, 630: 1597, 250: 253, 180: 775, 370: 2200, 190: 1792, 500: 1193, 620: 65, 870: 83, 170: 562, 330: 202, 980: 90, 520: 167, 200: 262, 670: 154, 540: 431, 420: 502, 320: 1635, 350: 141, 70: 399, 220: 281, 550: 31, 470: 143, 650: 733, 590: 207, 570: 177, 390: 273, 310: 248, 830: 9, 860: 167, 430: 246, 90: 293, 680: 308, 110: 185, 340: 304, 970: 30, 640: 154, 260: 168, 660: 146, 290: 127, 100: 111, 820: 138, 780: 100, 490: 13, 280: 162, 530: 77, 890: 343, 300: 68, 740: 13, 750: 10, 810: 28, 480: 181, 1010: 13, 950: 46, 800: 77, 690: 105, 900: 44, 440: 66, 510: 63, 1180: 12, 560: 129, 580: 130, 940: 22, 880: 33, 1250: 31, 840: 13, 700: 40, 730: 6, 760: 8, 960: 67, 1030: 51, 460: 46, 1040: 15, 990: 22, 770: 7, 710: 1, 1090: 4, 1320: 1, 1340: 13, 1420: 1, 1600: 2, 720: 9, 1280: 1, 1240: 2}
x = list(elevation_count.values())
x = [int(round(i/50)*50)+1 for i in x]
x = [math.log(i) for i in x]
y = list(elevation_count.keys())

plt.barh(y, x, height=50, color="green")
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
year_count = {2015: 50519, 2010: 12291, 2012: 21978, 2000: 7441, 2002: 5640, 2001: 10003, 2003: 9484, 2004: 9748, 2005: 11272, 2006: 11879, 2009: 11473, 2007: 15651, 2008: 12197, 2016: 89129, 2017: 87510, 2019: 98951, 2018: 102131, 2014: 40287, 2013: 30861, 2011: 15668, 2022: 9774, 2021: 46899, 2023: 1289, 2020: 43019}
y = list(year_count.values())
x = list(year_count.keys())

plt.barh(x, y, height=1, color="green")
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
month_count = {5: 19698, 11: 32111, 8: 29570, 1: 20956, 3: 25535, 7: 47973, 9: 12722, 10: 23245, 6: 43560, 12: 21987, 4: 19632, 2: 21509}
x = list(month_count.values())
y = list(month_count.keys())

plt.barh(y, x, height=1, color="green")
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