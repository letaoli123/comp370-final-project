import http.client
import json
import os
import urllib.parse
from pathlib import Path

from newsapi import NewsApiClient

from dotenv import load_dotenv

load_dotenv()
NEWS_API_ORG_KEY = os.getenv('NEWSAPI_ORG_KEY')


rootpath = Path(__file__).parent.parent
data_path = rootpath / "data"

collection_filepath = data_path / "mamdani_newsapi_org.json"
news_api = NewsApiClient(NEWS_API_ORG_KEY)
all_articles = news_api.get_everything(
    q='Zohran Mamdani',
    from_param='2025-10-14',
    to='2025-01-11',
    language='en',
    sort_by='relevancy',
    page=2
    )

# Decode and parse JSON
# Dump in JSON file
with open(collection_filepath, 'a', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

# print(f"Saved {len(news_data.ge)}")