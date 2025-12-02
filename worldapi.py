import json
import worldnewsapi
from worldnewsapi.rest import ApiException

API_KEY = "API KEY"

config = worldnewsapi.Configuration(api_key={"apiKey": API_KEY})
client = worldnewsapi.ApiClient(config)
newsapi = worldnewsapi.NewsApi(client)

all_articles = []
offset = 0

while offset < 500:
    try:
        response = newsapi.search_news(
            text="\"Zohran Mamdani\"",
            language="en",
            source_country="us",  # US sources only
            number=50,            # max per request
            offset=offset
        )
        articles = response.news
        if not articles:  # stop if no more articles
            break
        all_articles.extend(articles)
        offset += 50
    except ApiException as e:
        print(f"Error fetching news: {e}")
        break

# Save to JSON
with open("zohran_mamdani_us_articles.json", "w", encoding="utf-8") as f:
    json.dump([article.to_dict() for article in all_articles], f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_articles)} articles to 'zohran_mamdani_us_articles.json'")
