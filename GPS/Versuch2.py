import requests
import time
import pandas as pd
from datetime import timedelta

url = "https://api.gbif.org/v1/occurrence/search"
params = {
    "geometry": "POLYGON((-89.4082692 -0.6687503,-89.5922901 -0.7621268,-89.7049000 -0.9282769,-89.6197560 -1.0257664,-89.3450978 -0.9749624,-89.2256214 -0.8197996,-89.1926625 -0.6591379,-89.2764332 -0.6069561,-89.4082692 -0.6687503))",
    "taxonKey": "212",
    "hasCoordinate": "true",
    "hasGeospatialIssue":"false",
    "fromDate": "2000-01",
    "limit": "300",
    "fields":"species,vernacularName,decimalLatitude,decimalLongitude,elevation,month"
}


offset = 0
page_number = 1
unique_species = set()
i=0

while True:
    params["offset"] = offset
    start_time1 = time.monotonic()
    response = requests.get(url, params=params).json()
    end_time1 = time.monotonic()

    start_time2 = time.monotonic()
    if "results" not in response:
        break

    
    results = response["results"]
    
    for result in results:
        if i == 0:
            print(result)
            i += 1
        if "species" in result:
            unique_species.add(result["species"])
            #unique_species.add(result["vernacularName"])

    offset += 300
    page_number += 1

    if len(results) < 300:
        break
    end_time2 = time.monotonic()
    time_delta1 = timedelta(seconds=end_time1 - start_time1)
    page_time = str(time_delta1).split(".")[0]
    time_delta2 = timedelta(seconds=end_time2 - start_time2)
    rest_time = str(time_delta2).split(".")[0]
    print(f"Page {page_number} ({page_time}) ({rest_time})", end="\r")
print(f"\nTotal unique species found: {len(unique_species)}")

df = pd.DataFrame({"scientificName": list(unique_species)})
filename = "San Cristobal Island.csv"
df.to_csv(filename, index=False)

print(f"{len(unique_species)} unique species found. Data saved to {filename}.")

#GBIF.org (10 March 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.9k8afc
