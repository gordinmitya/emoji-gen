import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import os
from utils import emoji_to_hex_string


BASE_URL = 'https://emojipedia.org/'
FOLDER_RAW = 'data/wiki-raw'
FOLDER_DESCRIPTIONS = 'data/wiki-descriptions'
COLLECTIONS = [
    'smileys',
    'people',
    'nature',
    'food-drink',
    'activity',
    'travel-places',
    'objects',
    'symbols',
    'flags',
]


async def fetch_collection_json(session, collection):
    if os.path.exists(f'{FOLDER_RAW}{collection}.json'):
        print(f'{collection}.json already exists')
        with open(f'{FOLDER_RAW}{collection}.json') as json_file:
            return json.load(json_file)

    async with session.get(BASE_URL + collection) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
        if not script_tag:
            raise ValueError("Could not find the <script> tag with the specified id and type")
        json_content = script_tag.string
        return json.loads(json_content)


def find_descriptions_query(raw_data):
    for query in raw_data['props']['pageProps']['dehydratedState']['queries']:
        try:
            if len(query['state']['data']['subCategories']) > 0:
                return query['state']['data']
        except (KeyError, TypeError):
            pass
    raise ValueError("Could not find a query with subCategories")


def parse_json_descriptions(raw_data):
    data = find_descriptions_query(raw_data)
    count = 0
    for subcat in data['subCategories']:
        for emoji in subcat['emoji']:
            hex_string = emoji_to_hex_string(emoji['code'])
            bs = BeautifulSoup(emoji['description'], 'html.parser')
            txt_description = bs.get_text()
            with open(f'{FOLDER_DESCRIPTIONS}/{hex_string}.txt', 'w') as f:
                f.write(txt_description)
            count += 1
    print(f'Saved {count} descriptions for {data["slug"]}')


async def main():
    os.makedirs(FOLDER_RAW, exist_ok=True)
    os.makedirs(FOLDER_DESCRIPTIONS, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        for collection in COLLECTIONS:
            raw_data = await fetch_collection_json(session, collection)
            with open(f'{FOLDER_RAW}/{collection}.json', 'w') as f:
                json.dump(raw_data, f, indent=4)
            parse_json_descriptions(raw_data)


if __name__ == "__main__":
    asyncio.run(main())
