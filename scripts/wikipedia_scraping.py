import cloudscraper
from bs4 import BeautifulSoup
import time 
import json
import re
import pandas as pd

df = pd.read_csv('sesame_guest_stars.csv', dtype={'imdb id': str})

q_ids = []
imdb_ids = []

for url in df['wikipedia url']:
    if pd.notna(url):
        time.sleep(0.25)
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        lod = soup.find('script', {'type': "application/ld+json"})

        # Get Wikidata Q IDs from linked data
        if lod:
            lod_text = lod.text.strip()
            try:
                json_data = json.loads(lod_text)
                wikidata_link = json_data.get("sameAs")
                match = re.search(r'Q\d+', wikidata_link)

                if match:
                    q_id = match.group()
                    q_ids.append(q_id)
                else:
                    q_ids.append(None)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for {url}")
        
        # Get IMDb IDs
        imdb_id = None
        imdb_id_container = soup.find_all('li')
        for container in imdb_id_container:
            imdb_id_elems = container.find_all('a', href=re.compile(r'^https://www.imdb.com/name/nm\d+/'))
            for imdb_id_elem in imdb_id_elems:
                imdb_id_match = re.search(r'nm(\d+)/$', imdb_id_elem['href'])
                if imdb_id_match:
                    imdb_id = imdb_id_match.group(1)
        
        imdb_ids.append(imdb_id)
        
    else:
        q_ids.append(None)
        imdb_ids.append(None)


df['wikidata q id'] = q_ids
df['imdb id'] = imdb_ids

df.to_csv('sesame_guest_stars.csv', index=False)
