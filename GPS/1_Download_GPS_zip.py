import json
import requests
import time
import os
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

def ask_for_region_name():
    region_name=input("Region Name:  ")
    return region_name

def ask_for_coords():
    if input("Do you want to use custom coordinates ?  y/n: ").lower() == "y":
        coords = make_anticlockwise(json.loads(input("Insert the coordinates in a manner of [[lat1,lon1],[lat2,lon2],...] :  ")))
        coord_param = {'type': 'within', 'geometry': "POLYGON((" + ",".join([f"{coord[0]} {coord[1]}" for coord in coords]) + "))"}
    else:
        print("...Using default coordinates")
        coord_param = {'type': 'within', 'geometry':"POLYGON((-92.4582030 2.2909974, -92.4032648 -1.7612783, -87.4478408 -1.8491081, -87.6785812 2.2470951, -92.4582030 2.2909974))"}
        
    return coord_param

def ask_for_year():
    print("You have the option to gather data for a specific year or form starting year until now")
    if input("Do you want to use a specific year? y/n").lower() == "y":
        year = input("which year are you interested in ? :")
        year_param = {'type': 'equals', 'key': 'YEAR', 'value': year}
    else:
        year = input("which year do you want to start from :")
        year_param = {'type': 'greaterThanOrEquals', 'key': 'YEAR', 'value': year}
        
    return year_param

def get_download_key():
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

        # Define the API endpoint URL
        api_url = 'https://api.gbif.org/v1/occurrence/download/request'

        coord_param = ask_for_coords()
        year_param = ask_for_year()

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
                    year_param,
                    coord_param
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

    return download_key

def download_zip_file(region_name,download_key):

    # Check the download status
    status_url = f'https://api.gbif.org/v1/occurrence/download/{download_key}'
    #status_url = f'https://api.gbif.org/v1/occurrence/download/0079863-230224095556074'

    while True:
        response = requests.get(status_url)
        #check the request response
        if response.ok:
            #get the download status
            download_status = response.json()['status']

            if download_status == 'SUCCEEDED':
                print(f'\nDownload status: {download_status}')
                download_link = response.json()['downloadLink']
                print(f'Download URL: {download_link}')

                # Download the file and save it as a CSV
                with urllib.request.urlopen(download_link) as response:
                    file_size = int(response.headers['Content-Length'])

                print(f"File size: {round(file_size / (1024 * 1024), 2)} Megabytes")
                DownloadConfirmation = input("Would you like to download the occurrence data ? y/n: ")

                if DownloadConfirmation.lower() == "y":
                    print("Downloading...")
                    folder_path = f"Regions/{region_name}/"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    download_url(download_link, folder_path + f'{region_name}.zip')
                else:
                    print("Aborting download...")
                    time.sleep(5)
                break

            elif download_status == 'PREPARING' or download_status == 'RUNNING':
                seconds = 60
                print(f'\nDownload status: {download_status}  Check again in {seconds}s',end="\r")
                time.sleep(seconds)

            else:
                print(f'\nDownload status: {download_status}')
                break

        else:
            print('\nFailed to check download status')
            print(response.content)
            break



region_name= ask_for_region_name()

download_key = get_download_key()

download_zip_file(region_name=region_name,download_key=download_key)

