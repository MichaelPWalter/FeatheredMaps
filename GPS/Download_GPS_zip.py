import requests
import pandas as pd
import time
import urllib.request
from tqdm import tqdm


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def make_anticlockwise(coords):
    # Calculate the area using the Shoelace Formula
        area = 0
        for i in range(len(coords)):
            j = (i + 1) % len(coords)
            area += coords[i][0] * coords[j][1] - coords[j][0] * coords[i][1]

        # If the area is negative, the polygon is oriented clockwise
        if area < 0:
            coords.reverse()

        return coords

# Define the authentication credentials
if input("Do you have a download key yet ?  y/n: ").lower() == "y":
    download_key = input("download_key: ")
else:
    print("If you do not have a download_key yet you will generate a downloadable .zip file now")
    username = input("GBIF_Username: ")
    password = input("GBIF_Password: ")
    auth = (username,password)

    # Define the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Define the polygon WKT

    coords = make_anticlockwise([
      [
        -9.970093,
        29.386962
      ],
      [
        -8.747864,
        29.386962
      ],
      [
        -8.747864,
        30.668628
      ],
      [
        -9.970093,
        30.668628
      ],
      [
        -9.970093,
        29.386962
      ]
    ])

    

    #polygon_wkt = "POLYGON((-92.4582030 2.2909974, -92.4032648 -1.7612783, -87.4478408 -1.8491081, -87.6785812 2.2470951, -92.4582030 2.2909974))"
    polygon_wkt = "POLYGON((" + ",".join([f"{coord[0]} {coord[1]}" for coord in coords]) + "))"

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
            download_link = response.json()['downloadLink']
            print(f'Download URL: {download_link}')
            # Download the file and save it as a CSV
            with urllib.request.urlopen(download_link) as response:
                 file_size = int(response.headers['Content-Length'])
            print(f"File size: {round(file_size / (1024 * 1024), 2)} Megabytes")
            DownloadConfirmation = input("Would you like to download the occurrence data ? y/n: ")
            if DownloadConfirmation.lower() == "y":
                print("Downloading...")
                download_url(download_link, 'GPS/occurrences.zip')
            else:
                print("Aborting download...")
                time.sleep(5)
            break
        elif download_status == 'PREPARING' or download_status == 'RUNNING':
            seconds = 60
            print(f'Download status: {download_status}  Check again in {seconds}s')
            time.sleep(seconds)
        else:
            print(f'Download status: {download_status}')
            break
    else:
        print('Failed to check download status')
        print(response.content)
        break