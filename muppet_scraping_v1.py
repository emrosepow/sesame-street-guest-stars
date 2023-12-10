import csv
import requests
import cloudscraper
from bs4 import BeautifulSoup
import time

# NORMAL GUEST STAR LISTINGS: 1-39, 46, 48
# DIFFERENT GUEST STAR LISTINGS: 40, 41, 42, 43, 44, 45 (see muppet_scraping_v2.py)
# NO GUEST STAR LISTINGS: 47, 49-54

pages_to_scrape = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 46, 48]

field_names = ['name', 'season', 'wikipedia url', 'wikidata q id', 'imdb id', 'character name']

with open ('sesame_guest_stars.csv', 'w', newline='') as file: 
    csv_file = csv.DictWriter(file, fieldnames=field_names)

    csv_file.writeheader()

    for i in pages_to_scrape:
        time.sleep(2.25)
        page_url = f"https://muppet.fandom.com/wiki/Season_{i}"
        scraper = cloudscraper.create_scraper()
        page = scraper.get(page_url)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        season = soup.find('span', {'class': "mw-page-title-main"}).text.strip()
        print(season)

        dl_elements = soup.find_all("dl")

        # Find all <dt> and <dd> elements in <dl>
        full_cast = []
        dl_data = []
        for dl_element in dl_elements:
            dt_elements = dl_element.find_all('dt')
            dd_elements = dl_element.find_all('dd')
        
            dl_entry = {
                'dt_elements': dt_elements,
                'dd_elements': dd_elements
            }

            dl_data.append(dl_entry)

        full_cast.append(dl_data)

        # Create a list to store <dd> elements
        guest_star_links = []
        for entry in full_cast:
            for dl_data in entry:
                for dt_element, dd_element in zip(dl_data['dt_elements'], dl_data['dd_elements']):
                    if 'Guest Stars' in dt_element.text:
                        guest_star_links.extend(dd_element.find_all('a'))
            
            # Iterate through individual guest star pages
            celeb_data = []
            for link_element in guest_star_links:
                time.sleep(0.25)
                link = link_element.get('href')
                celeb_url = f"https://muppet.fandom.com{link}"
                title = link_element.text

                if link.startswith('/wiki/'):
                    celeb_url = celeb_url
                else: 
                    celeb_url = None

                page_title = None
                if celeb_url:
                    page = requests.get(celeb_url)
                    soup = BeautifulSoup(page.text, 'html.parser')
                
                    title_elem = soup.find('b')
                    if title_elem:
                        title = title_elem.text.strip()

                wikipedia_url = None        
                wikipedia_url_container = soup.find_all('b')
                for container in wikipedia_url_container:
                    wikipedia_url_elem = container.find('a')
                    if wikipedia_url_elem:
                        wikipedia_url = wikipedia_url_elem['href']

                celeb_dict = {
                    'name': title,
                    'season': season,
                    'wikipedia url': wikipedia_url,
                    }
            
                if title:
                    celeb_data.append(celeb_dict)

            csv_file.writerows(celeb_data)
