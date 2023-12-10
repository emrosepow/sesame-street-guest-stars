import imdb
import pandas as pd

character_names = []

df = pd.read_csv('sesame_guest_stars.csv', dtype={'imdb id': str})

ia = imdb.IMDb()

ss_id = '0063951' # IMDb ID for Sesame Street

for index, row in df.iterrows():
    imdb_id = str(row['imdb id'])

    character_name = None
    # Skip if IMDb ID is missing or not in the expected format
    if pd.isna(imdb_id) or imdb_id.lower() == 'nan':
        print(f"Skipping missing IMDb ID for {row['name']}")

    # Get person information from IMDb
    elif imdb_id:
        try:
            actor = ia.get_person(imdb_id)
            print(f"Actor: {actor['name']} (IMDb ID: {imdb_id})")

        # Iterate through filmography, find Sesame Street, and print roles
            for role_type in ['actress', 'actor']:
                if role_type in actor['filmography']:
                    for movie in actor['filmography'][role_type]:
                        if movie.movieID == ss_id:
                            character_name = movie.currentRole
                            print(f"Movie: {movie['title']}, Role: {character_name}, Role Type: {role_type.capitalize()}")
                            break

        except imdb.IMDbError as e:
            print(f"Error fetching IMDb data for {imdb_id}: {e}")
    
    character_names.append(character_name)
    print(f"Character Name for {row['name']}: {character_name}")

if len(character_names) != len(df):
    raise ValueError(f"Length of character_names ({len(character_names)}) does not match the length of the DataFrame ({len(df)})")

df['character name'] = character_names

df.to_csv('sesame_guest_stars.csv', index=False)
