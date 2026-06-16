import feedparser
import requests
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

RSS_FEEDS = [
    {"name": "The Hindu", "url": "https://www.thehindu.com/feeder/default.rss"},
    {"name": "Times of India", "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"},
    {"name": "Indian Express", "url": "https://indianexpress.com/feed/"},
    {"name": "NDTV", "url": "https://feeds.feedburner.com/ndtvnews-top-stories"},
]

def fetch_from_rss():
    all_articles = []

    for paper in RSS_FEEDS:
        try:
            feed = feedparser.parse(paper["url"])
            print(f"✅ {paper['name']}: {len(feed.entries)} articles fetched")

            for entry in feed.entries:
                article = {
                    "newspaper": paper["name"],
                    "title": entry.get("title", "No title"),
                    "description": entry.get("summary", ""),
                    "content": entry.get("summary", ""),
                    "published_at": entry.get("published", ""),
                    "url": entry.get("link", "")
                }
                all_articles.append(article)

        except Exception as e:
            print(f"❌ {paper['name']}: Failed — {e}")

    return all_articles

def fetch_from_newsapi():
    all_articles = []

    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "in",
            "apiKey": NEWSAPI_KEY,
            "pageSize": 100
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            print(f"✅ NewsAPI: {len(articles)} articles fetched")

            for article in articles:
                cleaned = {
                    "newspaper": article.get("source", {}).get("name", "Unknown"),
                    "title": article.get("title", "No title"),
                    "description": article.get("description", ""),
                    "content": article.get("content", ""),
                    "published_at": article.get("publishedAt", ""),
                    "url": article.get("url", ""),
                    "image_url": article.get("urlToImage", "")
                }
                all_articles.append(cleaned)
        else:
            print(f"❌ NewsAPI: Status {response.status_code}")

    except Exception as e:
        print(f"❌ NewsAPI: Failed — {e}")

    return all_articles

def fetch_all_newspapers():
    print("🗞️ Starting newspaper fetch...")

    rss_articles = fetch_from_rss()
    api_articles = fetch_from_newsapi()

    all_articles = rss_articles + api_articles
    print(f"✅ Total articles fetched: {len(all_articles)}")

    return all_articles
    