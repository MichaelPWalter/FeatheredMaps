import csv

def get_common_names(scientific_names):
    common_names = []
    with open("taxonomy\\Avian_taxonomy.csv", "r", encoding="ISO-8859-1") as f:
        reader = csv.DictReader(f, delimiter=",")
        bird_map = {row["Species (Scientific)"]: row["Species (English)"] for row in reader}
        for scientific_name in scientific_names:
            common_names.append(bird_map.get(scientific_name, None))
    return common_names
#scientific_names = ["Struthio camelus", "Apteryx haastii", "Dromaius novaehollandiae", "XXXX"]
#print(get_common_names(scientific_names))


def get_scientific_names(common_names):
    scientific_names = []
    with open("taxonomy\\Avian_taxonomy.csv", "r", encoding="ISO-8859-1") as f:
        reader = csv.DictReader(f, delimiter=",")
        bird_map = {row["Species (English)"]: row["Species (Scientific)"] for row in reader}
        for common_name in common_names:
            scientific_names.append(bird_map.get(common_name, None))
    return scientific_names
common_names = ['Common Ostrich', 'Great Spotted Kiwi', 'Emu', 'XXXX']
print(get_scientific_names(common_names))

"""

def get_common_names(scientific_names):
This line defines a function called get_common_names that takes one argument, scientific_names, which is a list of scientific names of birds.

common_names = [] 
This line creates an empty list called common_names that will store the common names of birds.

with open("birds.csv", "r") as f: 
This line opens the file birds.csv in read mode ("r") and assigns the file object to f. The with statement is used to ensure that the file is automatically closed after the indented block is executed.

reader = csv.DictReader(f, delimiter=",")
This line creates a csv.DictReader object that reads the data from the file f. The delimiter argument is set to "," since the file is separated by commas.

bird_map = {row["Species (Scientific)"]: row["Species (English)"] for row in reader} 
This line creates a dictionary called bird_map that maps scientific names to common names. The dictionary comprehension iterates over each row in the reader object, and for each row, it creates a key-value pair in the dictionary where the key is the value of the "Species (Scientific)" field and the value is the value of the "Species (English)" field.

for scientific_name in scientific_names:
This line starts a for loop that iterates over the scientific names in the scientific_names list.

common_names.append(bird_map.get(scientific_name, None)) 
This line appends the common name of the bird to the common_names list. The bird_map.get method is used to retrieve the value of the scientific name in the bird_map dictionary. If the scientific name is not found in the dictionary, the get method returns the default value "Scientific name not found".

return common_names 
This line returns the common_names list, which contains the common names of birds corresponding to the scientific names in the scientific_names list.


https://birdsoftheworld.org/bow/specieslist
GBIF.org (06 February 2023) GBIF Occurrence Download  https://doi.org/10.15468/dl.ppu5hs


"""
