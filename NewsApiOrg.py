import http.client
import json
import os
import urllib.parse
from dotenv import load_dotenv


conn = http.client.HTTPSConnection("newsapi.org")
output_file = "test_us_news_articles.json"
all_articles = []

# -----------------------------
# Free-plan US sources (12)
# -----------------------------
US_SOURCES = [
    "cnn",
    "abc-news",
    "fox-news",
    "nbc-news",
    "usa-today",
    "the-verge",
    "reuters",
    "bloomberg",
    "politico",
    "cbs-news",
    "the-washington-post",
    "business-insider"
]
source_string = ",".join(US_SOURCES)

# -----------------------------
# User-Agent header (required)
# -----------------------------
headers = {
    "User-Agent": "comp370-final-project/1.0"
}

# -----------------------------
# Pagination settings
# -----------------------------
PAGE_SIZE = 100  # max allowed
MAX_PAGES = 10   # try up to 10 pages (1000 articles max)
FROM_DATE = "2025-01-01"

for page in range(1, MAX_PAGES + 1):
    params = urllib.parse.urlencode({
        "apiKey": API_KEY,
        "sources": source_string,
        "pageSize": PAGE_SIZE,
        "page": page,
        "from": FROM_DATE
    })

    conn.request("GET", f"/v2/top-headlines?{params}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    news_json = json.loads(data)

    if news_json.get("status") == "error":
        print("API error:", news_json)
        break

    articles = news_json.get("articles", [])
    if not articles:
        print(f"No more articles at page {page}.")
        break

    all_articles.extend(articles)
    print(f"Page {page}: collected {len(articles)} articles")

# -----------------------------
# Save all articles to JSON
# -----------------------------
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"\nSaved {len(all_articles)} total articles to {output_file}")
