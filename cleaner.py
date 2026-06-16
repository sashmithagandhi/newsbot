def clean_article(article):
    title = article.get("title") or "No title"
    description = article.get("description") or ""
    content = article.get("content") or description
    published_at = article.get("published_at") or ""
    url = article.get("url") or ""
    newspaper = article.get("newspaper") or "Unknown"

    # Remove None values and extra whitespace
    title = title.strip()
    description = description.strip()
    content = content.strip()

    # Skip articles with no title or content
    if title == "No title" and content == "":
        return None

    return {
        "newspaper": newspaper,
        "title": title,
        "description": description,
        "content": content,
        "published_at": published_at,
        "url": url
    }

def clean_all_articles(raw_articles):
    cleaned = []

    for article in raw_articles:
        result = clean_article(article)
        if result:
            cleaned.append(result)

    print(f"✅ Cleaned {len(cleaned)} articles out of {len(raw_articles)}")
    return cleaned
    