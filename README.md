# Neighbors on the Street: An Exploration of Guest Stars on Sesame Street

Final project for INFO-664: Programming for Cultural Heritage <br />
By Emma Powell, Pratt MSLIS '24
<br /><br />
This project looks to explore representation on _Sesame Street_ through the guest stars over time. The data captures demographic information relating to gender, ethnicity, and sexuality, as well as further information on occupation, religion, military branch, and more. All of the data is collected through crowdsourced information hubs of [Muppet Wiki](https://muppet.fandom.com/wiki/Muppet_Wiki), Wikipedia, IMDb, and Wikidata, making it less thorough than ideal.<br />
You can view the visualization [here](https://public.tableau.com/views/NeighborsontheStreet/Dashboard2?:language=en-US&:display_count=n&:origin=viz_share_link). 
# Data
_sesame-street-guest-stars/data_<br />
Data is collected from scraping Muppet Wiki and Wikipedia, the Cinemagoer Python package, and Wikidata API.<br />
<br />
**.../sesame_guest_stars.csv**<br />
CSV file containing list of names from Muppet Wiki, corresponding identifiers from Wikipedia, and character names from IMDb.<br /><br />
**.../sesame_guest_stars_revised_csv.txt**<br />
Cleaned data from `sesame_guest_stars_updated.csv` through Open Refine, now stored as CSV data in a TXT file.<br /><br />
**.../sesame_guest_stars_updated.csv**<br />
CSV file containing all data pulled from Wikidata API alongside data from `sesame_guest_stars.csv`.<br /><br />
# Python Scripts
_sesame-street-guest-stars/scripts_<br />
Group of Python scripts used to find all necessary data. They are listed below in the correct order to run, as the scripts build off each other. <br />
<br />
**.../muppet_scraping_v1.py**<br />
A script to build the base list of guest stars. Scrapes Muppet Wiki for Seasons 1-39, 46, and 48. Requests name of guest star, respective season, and Wikipedia link. (Note: At time of creation, Seasons 40-45 list guest stars in a different structure and Seasons 47, 49-54 do not have a full list of guest stars)<br /><br />
**.../muppet_scraping_v2.py**<br />
Builds of base list of guest stars with Seasons 40-45 due to different structure.<br /><br />
**.../wikipedia_scraping.py**<br />
Scrapes Wikipedia using Wikipedia links from Muppet Wiki scrape. Finds Wikidata QIDs and IMDb IDs.<br /><br />
**.../get_imdb.py**<br />
Uses Cinemagoer and IMDb ID to find character name on _Sesame Street_ for guest stars.<br /><br />
**.../get_wikidata.py**<br />
Requests information from Wikidata with Wikidata QID for the following properties: instance of, gender, occupation, creator, from narrative universe, country of citizenship, sexual orientation, ethnic group, religion, convicted of, military branch, country of origin, has part(s).
