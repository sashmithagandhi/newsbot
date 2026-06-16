from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from fetcher import fetch_all_newspapers
from cleaner import clean_all_articles
from chatbot import store_articles_in_chromadb
from database import SessionLocal
from models import Article, Alert, User
from notifier import send_morning_digest

def fetch_and_store():
    print(f"🗞️ {datetime.now()} — Starting scheduled newspaper fetch")

    # Step 1 — Fetch
    raw_articles = fetch_all_newspapers()

    # Step 2 — Clean
    cleaned_articles = clean_all_articles(raw_articles)

    # Step 3 — Save to MySQL
    db = SessionLocal()
    try:
        for article in cleaned_articles:
            new_article = Article(
                newspaper_name=article["newspaper"],
                title=article["title"],
                description=article["description"],
                content=article["content"],
                published_at=article["published_at"],
                url=article["url"],
                image_url=article.get("image_url", "")
            )
            db.add(new_article)

        # Step 4 — Create alert
        alert = Alert(
            message=f"Today's newspapers are ready — {datetime.now().strftime('%d %B %Y')}"
        )
        db.add(alert)
        db.commit()
        print(f"✅ Saved {len(cleaned_articles)} articles to MySQL")

    except Exception as e:
        print(f"❌ Database error: {e}")
        db.rollback()
    finally:
        db.close()

    # Step 4.5 — Send morning emails
    db2 = SessionLocal()
    try:
        users = db2.query(User).all()
        if users:
            newspaper_counts = {}
            for article in cleaned_articles:
                name = article["newspaper"]
                newspaper_counts[name] = newspaper_counts.get(name, 0) + 1

            summary_lines = [f"{name} — {count} articles" for name, count in newspaper_counts.items()]
            summary = "\n".join(summary_lines)

            send_morning_digest(users, summary)
        else:
            print("ℹ️ No registered users — skipping email notifications")
    except Exception as e:
        print(f"❌ Email notification error: {e}")
    finally:
        db2.close()

    # Step 5 — Store in ChromaDB for AI
    store_articles_in_chromadb(cleaned_articles)
    print(f"✅ {datetime.now()} — Fetch complete")

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        fetch_and_store,
        trigger="cron",
        hour=7,
        minute=0
    )

    scheduler.start()
    print("✅ Scheduler started — newspapers will be fetched at 7AM daily")
    return scheduler