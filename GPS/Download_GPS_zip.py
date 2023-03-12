import requests
import pandas as pd
import time
import urllib.request

# Define the polygon WKT
polygon_wkt = "POLYGON((-92.4582030 2.2909974, -92.4032648 -1.7612783, -87.4478408 -1.8491081, -87.6785812 2.2470951, -92.4582030 2.2909974))"

# Define the API endpoint URL
api_url = 'https://api.gbif.org/v1/occurrence/download/request'

# Define the download parameters
params = {
    'creator': 'erdenfeuer',
    'format': 'SIMPLE_CSV',
    'predicate': {
        'type': 'and',
        'predicates': [
            {'type': 'equals', 'key': 'TAXON_KEY', 'value': '212'},
            #{'type': 'equals', 'key': 'BASIS_OF_RECORD', 'value': 'HUMAN_OBSERVATION'},
            {'type': 'equals', 'key': 'HAS_COORDINATE', 'value': 'true'},
            {'type': 'greaterThanOrEquals', 'key': 'YEAR', 'value': '2000'},
            #{'type': 'equals', 'key': 'YEAR', 'value': '2000'},
            {'type': 'within', 'geometry': polygon_wkt}
        ]
    }
}

# Define the authentication credentials
username = input("GBIF_Username: ")
password = input("GBIF_Password: ")
auth = (username,password)

# Define the headers
headers = {
    'Content-Type': 'application/json'
}

 
# Send the download request and retrieve the download key
response = requests.post(api_url, json=params, auth=auth, headers=headers)

print(f'Response status code: {response.status_code}')
#print(f'Response content: {response.content}')

if response.ok:
    download_key = response.content.decode()
    #print(download_key)
    print(f'Download key: {download_key}')
else:
    print('Failed to initiate download')
    print(response.content)

# Check the download status
status_url = f'https://api.gbif.org/v1/occurrence/download/{download_key}'
#status_url = f'https://api.gbif.org/v1/occurrence/download/0079863-230224095556074'

while True:
    response = requests.get(status_url)
    if response.ok:
        download_status = response.json()['status']
        if download_status == 'SUCCEEDED':
            print(f'Download status: {download_status}')
            download_url = response.json()['downloadLink']
            print(f'Download URL: {download_url}')
            # Download the file and save it as a CSV
            with urllib.request.urlopen(download_url) as response:
                 file_size = int(response.headers['Content-Length'])
            print(f"File size: {round(file_size / (1024 * 1024), 2)} Megabytes")
            print("Downloading...")
            urllib.request.urlretrieve(download_url, 'GPS/occurrences.zip')
            break
        elif download_status == 'PREPARING' or download_status == 'RUNNING':
            print(f'Download status: {download_status}')
            time.sleep(60)
        else:
            print(f'Download status: {download_status}')
            break
    else:
        print('Failed to check download status')
        print(response.content)
        break