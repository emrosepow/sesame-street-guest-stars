import csv
import requests
import cloudscraper
from bs4 import BeautifulSoup
import time

pages_to_scrape = [40, 41, 42, 43, 44, 45]

field_names = ['name', 'season', 'wikipedia url', 'wikidata q id', 'imdb id', 'character name']

with open ('sesame_guest_stars.csv', 'a', newline='') as file: 
    csv_file = csv.DictWriter(file, fieldnames=field_names)

    for i in pages_to_scrape:
        time.sleep(2.25)
        page_url = f"https://muppet.fandom.com/wiki/Season_{i}"
        scraper = cloudscraper.create_scraper()
        page = scraper.get(page_url)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        season = soup.find('span', {'class': "mw-page-title-main"}).text.strip()
        print(season)

        link_container = soup.select('table.columnlist ul li a')

        title = [a['title'] for a in link_container]

        guest_star_links = [a['href'] for a in link_container]

        celeb_data = []
        for link_element in guest_star_links:
            time.sleep(0.25)
            celeb_url = f"https://muppet.fandom.com{link_element}"

            if link_element.startswith('/wiki/'):
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
