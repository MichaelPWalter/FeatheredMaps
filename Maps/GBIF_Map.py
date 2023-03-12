import requests

# Define the API endpoint and query parameters

params = {
    'srs': 'EPSG:4326',
    'params': 'binomial:Passer domesticus&geo_field=coordinates&geometry=POLYGON((-92.4582030 2.2909974, -92.4032648 -1.7612783, -87.4478408 -1.8491081, -87.6785812 2.2470951, -92.4582030 2.2909974))&style=points&colors=#0000ff'
}

x=15
y=15
z=15
endpoint=f"https://api.gbif.org/v2/map/occurrence/density/4/5/5@4x.png?taxonKey=212&basisOfRecord=HUMAN_OBSERVATION&years=2000,2023&bin=square&squareSize=512&style=purpleYellow.point"
"https://api.gbif.org/v2/map/occurrence/adhoc/{z}/{x}/{y}@5x.png?srs=EPSG:4326&style=purpleYellow.point&bin=square&squareSize=1&month=1"
# Send the API request and save the response as a file
#response = requests.get(endpoint, params=params)
response = requests.get(endpoint)
print(response)
with open('map.jpg', 'wb') as f:
    f.write(response.content)