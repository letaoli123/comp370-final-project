import http.client
import json
import os
import urllib.parse

from dotenv import load_dotenv

load_dotenv()
News_API_Key = os.getenv('NewsAPI_KEY')
conn = http.client.HTTPSConnection('api.thenewsapi.com')

params = urllib.parse.urlencode({
    'api_token': News_API_Key,
    'search': 'Zohran Mamdani',
    'search_fields': 'title,description,keywords,main_text',
    'locale': 'us,ca',
    'limit': 3,
    'published_after': '2025-01',
    'language': 'en',
    'page': 1
    })

# GET request
conn.request('GET', '/v1/news/all?{}'.format(params))
res = conn.getresponse()
data = res.read()

# Decode and parse JSON
news_data = json.loads(data.decode('utf-8'))

# Dump in JSON file
with open('zohran_mamdani_news.json', 'a', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print(f"Saved {len(news_data.get('data', []))} English articles mentioning Zohran Mamdani to zohran_mamdani_news.json")
