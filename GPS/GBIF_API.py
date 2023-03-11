import requests

# Define the API endpoint
url = 'https://api.gbif.org/v1/occurrence/search'

url2 = 'https://api.gbif.org/v1/occurrence/count'

# Set the search parameters
params = {
    'geometry': "POLYGON((-91.9447588 -1.5833337,-89.2003480 -1.5160661,-89.1446439 0.8500891,-91.8744660 0.7833087,-91.9447588 -1.5833337))",
    'taxonKey': 212, # taxon key for birds
    #'hasCoordinate': True,
    'limit': 1000000000 # set the maximum number of records to return
}



# Make the API request
response = requests.get(url, params=params)

# Check the status code of the response
if response.status_code == 200:
    # The request was successful
    data = response.json() # parse the response as JSON

    # Get the unique bird species from the results
    species = set([result['species'] for result in data['results'] if 'species' in result])

    # Print the list of unique bird species
    print(f"Found {len(species)} bird species:")
    for sp in species:
       print(sp)
else:
    # There was an error with the request
    print(f"Error: {response.status_code} {response.reason}")

"""
# Make the request to get the total number of occurrences
response = requests.get(url2, params=params)

# Check the status code of the response
if response.status_code == 200:
    # The request was successful
    data = response.json() # parse the response as JSON

    # Get the total number of occurrences
    print(data)
    total = data['count']

    # Print the total number of occurrences
    print(f"Found {total} bird occurrences.")
else:
    # There was an error with the request
    print(f"Error: {response.status_code} {response.reason}")

"""