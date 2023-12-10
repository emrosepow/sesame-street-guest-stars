import requests
import re
import pandas as pd

df = pd.read_csv('sesame_guest_stars.csv')

data_list = []

# Function to get label from Wikidata API
def get_label(entity_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={entity_id}&languages=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('entities', {}).get(entity_id, {})
        label = data.get('labels', {}).get('en', {}).get('value')
        return label
    return None

# Properties mapping between Wikidata properties and column names
properties_mapping = {
    'P31': 'instance of',
    'P21': 'gender',
    'P106': 'occupation',
    'P170': 'creator',
    'P1080': 'from narrative universe',
    'P27': 'country of citizenship',
    'P91': 'sexual orientation',
    'P172': 'ethnic group',
    'P140': 'religion',
    'P1399': 'convicted of',
    'P241': 'military branch',
    'P495': 'country of origin',
    'P527': 'has part(s)'
}

# Assuming df['wikidata q id'] contains the QIDs
for index, row in df.iterrows():
    q_id = row['wikidata q id']

    # Check if Q ID is available
    if pd.notna(q_id):
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={q_id}&sites=enwiki&props=info%7Csitelinks%7Caliases%7Clabels%7Cdescriptions%7Cclaims%7Cdatatype&languages=en&normalize=1&formatversion=2"

        find_q_id = re.compile(r'https://www\.wikidata\.org/w/api\.php\?action=wbgetentities&format=json&ids=Q\d+&sites=enwiki&props=info%7Csitelinks%7Caliases%7Clabels%7Cdescriptions%7Cclaims%7Cdatatype&languages=en&normalize=1&formatversion=2')

        valid_url = find_q_id.search(url)

        if valid_url:
            full_url = valid_url.group()

            # Make a request to Wikidata
            response = requests.get(full_url)

            if response.status_code == 200:
                data = response.json().get('entities', {}).get(q_id, {})

                # Extract the description value
                description = data.get('descriptions', {}).get('en', {}).get('value')

                # Dictionary to store the values of desired properties
                labels = {'Description': description}

                # Extract values for each property using the properties_mapping
                for prop, column_name in properties_mapping.items():
                    prop_values = data.get('claims', {}).get(prop, [])
                    prop_labels = [get_label(value.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id')) for value in prop_values]
                    labels[column_name] = ', '.join(str(label) for label in prop_labels if label is not None)

                print(labels)
                data_list.append(labels)

            else:
                print(f"Failed to retrieve data for QID: {q_id}")

        else:
            print("No match found.")
    else:
        # Fill the corresponding columns with None for rows without Q IDs
        labels = {'Description': None}
        for _, column_name in properties_mapping.items():
            labels[column_name] = None
        data_list.append(labels)

# Convert data_list to DataFrame
wikidata_df = pd.DataFrame(data_list)

# Concatenate the original DataFrame (df) with the new DataFrame (wikidata_df)
result_df = pd.concat([df, wikidata_df], axis=1)

# Write the updated DataFrame to new CSV file copy
result_df.to_csv('sesame_guest_stars_updated.csv', index=False)
