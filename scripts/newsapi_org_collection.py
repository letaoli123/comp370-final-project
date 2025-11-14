import http.client
import json
import os
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv

rootpath = Path(__file__).parent.parent
data_path = rootpath / "data"

collection_filepath = data_path / "mamdani_newsapi_org.json"
load_dotenv()
news_api_org_key = os.getenv('NEWSAPI_ORG_KEY')
conn = http.client.HTTPSConnection('newsapi.org')

params = urllib.parse.urlencode({
    'apiKey': news_api_org_key,
    'q': 'Zohran Mamdani',
    'from': '2024-11-01',
    'to': '2025-11-01',
    'sortBy': 'publishedAt',
    'language': 'en'
})

# GET request
conn.request('GET', '/v2/everything?{}'.format(params))
res = conn.getresponse()
data = res.read()

# Decode and parse JSON
news_data = json.loads(data.decode('utf-8'))

# Dump in JSON file
with open(collection_filepath, 'a', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

# print(f"Saved {len(news_data.ge)}")