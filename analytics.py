from collections import Counter
import re
from models import Article
from database import SessionLocal

STOPWORDS = set([
    "the", "a", "an", "is", "in", "on", "at", "to", "for",
    "of", "and", "or", "but", "with", "this", "that", "are",
    "was", "were", "has", "have", "had", "be", "been", "will",
    "from", "by", "as", "it", "its", "he", "she", "they", "we",
    "his", "her", "their", "our", "said", "says", "also", "after",
    "about", "into", "more", "than", "when", "which", "who", "what",
    "your", "after", "before", "over", "under", "news", "report"
])

def categorize_article(title):
    title_lower = title.lower()
    if any(w in title_lower for w in ["cricket", "football", "sports", "ipl", "match", "player", "goal", "tournament", "olympic"]):
        return "Sports"
    elif any(w in title_lower for w in ["market", "sensex", "economy", "gdp", "rupee", "stock", "business", "trade", "inflation"]):
        return "Business"
    elif any(w in title_lower for w in ["election", "minister", "parliament", "government", "party", "politics", "vote", "congress", "bjp"]):
        return "Politics"
    elif any(w in title_lower for w in ["war", "attack", "trump", "china", "russia", "ukraine", "iran", "israel", "nato", "military"]):
        return "World"
    elif any(w in title_lower for w in ["rain", "flood", "earthquake", "weather", "storm", "cyclone", "drought"]):
        return "Weather"
    elif any(w in title_lower for w in ["film", "movie", "actor", "actress", "bollywood", "music", "celebrity", "entertainment"]):
        return "Entertainment"
    else:
        return "General"

def get_trending_topics(articles):
    all_words = []
    for article in articles:
        text = f"{article.title} {article.description or ''}"
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        words = [w for w in words if w not in STOPWORDS]
        all_words.extend(words)
    counter = Counter(all_words)
    return [{"word": word, "count": count} for word, count in counter.most_common(10)]

def get_newspaper_activity(articles):
    counter = Counter([a.newspaper_name for a in articles])
    return [{"newspaper": name, "articles": count} for name, count in counter.most_common()]

def get_category_breakdown(articles):
    categories = [categorize_article(a.title) for a in articles]
    counter = Counter(categories)
    return [{"category": cat, "count": count} for cat, count in counter.most_common()]

def get_analytics():
    db = SessionLocal()
    try:
        articles = db.query(Article).order_by(Article.fetched_at.desc()).limit(200).all()
        return {
            "total_articles": len(articles),
            "trending_topics": get_trending_topics(articles),
            "newspaper_activity": get_newspaper_activity(articles),
            "category_breakdown": get_category_breakdown(articles)
        }
    finally:
        db.close()