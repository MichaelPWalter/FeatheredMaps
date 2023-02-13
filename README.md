# FeatheredMaps
Customizable Field Guides for Birders Worldwide


Started by Michael Walter in Feb2023 out of the need for a standardized print work for all localities worldwide. 

"I had planned a trip to Marocco and Western Sahara in May and i was unable to find field guides in paper format for the Area.
There were some books avaialable but they were from small companies and i wanted a book publisher i was used to.
I tried to explain the lack of publisher interest with the lack of english speaking birders in West Africa.
It also seemed that large areas (e.g. the whole of Europe) were being clumped together.
I really dont need to know what birds are common in a very localized spot in southern turkey when im only interested in German avifauna."

The goal is to create three pages for every single bird species: 
- A4 sized: Maximum detail, full page, portrait, for at home or at base camp
- A5 sized: Half detail, full page, portrait, for field guide
- A6 sized, Low detail, half page, landscape orientation, for condensed field guide

#Thinking about this it is very likely that people will have personal preferences.
#It would be cool to have a webapp that can wrap the information onto the pdf as the user decides in config file
# config files can then be adjusted and shared by other users

eBird and other online resources have the databases to create a very localized snapshot of the avifauna in every region on earth.
The information will be scraped and automatically assembled into a pdf for a chosen locality (country,region or custom map)
Sources are:
- ebird.org: Description and Images
- gbif.org: GPS-Data on sightings
- iucnredlist.org: Description, Vulnerability, population size, habitat


Here are the steps to make this happen:

Scrape and filter the information for every species

Create up to date (last 30 years) range maps for every species

Create pages for every species

Write a GUI that lets users choose an area of the world and field guide size:
- gather the necessary birds for this region form GPS-data
- let user choose the completeness of the data common, uncommon, rare and vagrant(100%)
- down the road subspecies could be inntroduced

Assemble Pdf for digital or print: 


Advantages:
- Every book is structured the same and is thus familiar for travel
- Books can be updated yearly and will most likely have the most accurate range maps available,
- As long as the number of sightings increases year over year the range maps will become more accurate every year.
- Books can be extremely localized (just for 1 city if enough sightings are available)
- Books would be extremely easy to create once the process is proven to work
- pdfs could be free and thus contribute to citzen science where the pages are corrected by users.

- If the field guides can deliver a quality close to tradional literature, i dont see why they could not take over a significant market share



