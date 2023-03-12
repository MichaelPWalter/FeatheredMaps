import requests
import time
import pandas as pd
from datetime import timedelta

url = "https://api.gbif.org/v1/occurrence/search"
params = {
    "geometry": "POLYGON((-92.4582030 2.2909974, -92.4032648 -1.7612783, -87.4478408 -1.8491081, -87.6785812 2.2470951, -92.4582030 2.2909974))",
    "taxonKey": "212",
    "hasCoordinate": "true",
    "fromDate": "2000-01",
    "limit": "300",
    "occuranceStatus" : "PRESENT"
}

filename = "GPS/Galápagos.csv"
header_written = False

offset = 100000
page_number = 1
unique_species = set()
results_list = []
i=0
year,month,day,decimalLongitude,decimalLatitude,elevation,level0,level1,level2,level3 = "","","","","","","","","",""
start_time0 = time.monotonic()

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
        #if i == 0:
        #    print(result)
        #    i += 1
        if "species" in result:
            species_name = result["species"]
            unique_species.add(species_name)

            for var in ["year","month","day","elevation"]:
                try: 
                    exec(f"{var} = int(result['{var}'])")
                except:
                    exec(f"{var} = ''")
            for var in ["decimalLongitude","decimalLatitude"]:
                try: 
                    exec(f"{var} = result['{var}']")
                except:
                    exec(f"{var} = ''")
            for var in ["level0","level1","level2","level3"]:
                try: 
                    exec(f"{var} = result['gadm']['{var}']['name']")
                except:
                    exec(f"{var} = ''")
                
            result_dict = {"species": species_name, 
                           "Longitude": decimalLongitude, 
                           "Latitude": decimalLatitude,
                           "elevation":elevation, 
                           "year": year, 
                           "month": month, 
                           "day": day,  
                           "LocLevel0": level0, 
                           "LocLevel1": level1, 
                           "LocLevel2": level2, 
                           "LocLevel3": level3  
                           }
            results_list.append(result_dict)

    offset += 300
    page_number += 1

    end_time2 = time.monotonic()
    time_delta1 = timedelta(seconds=end_time1 - start_time1)
    page_time = str(time_delta1).split(".")[0]
    time_delta2 = timedelta(seconds=end_time2 - start_time2)
    rest_time = str(time_delta2).split(".")[0]
    end_time0 = time.monotonic()
    time_delta0 = timedelta(seconds=end_time0 - start_time0)
    full_time = str(time_delta0).split(".")[0]
    print(f"Page {page_number} Retrived {offset*page_number} Results Current Retrieval: {page_time}  Current Processing: {rest_time}  Full time: {full_time}", end="\r")
    
    # write the results to the CSV file
    if not header_written:
        pd.DataFrame(results_list).to_csv(filename, index=False)
        header_written = True
    else:
        pd.DataFrame(results_list).to_csv(filename, mode="a", index=False, header=False)

    # clear the DataFrame to save memory
    del results_list
    results_list = []

    if len(results) < 300:
        break


print(f"{len(unique_species)} unique species found. Data saved to '{filename}'. Acquisition time: ({full_time})")


#GBIF.org (10 March 2023) GBIF Occurrence Download https://doi.org/10.15468/dl.9k8afc
