from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Article, Alert, Feedback, User
from chatbot import answer_question
from scheduler import start_scheduler, fetch_and_store
from analytics import get_analytics
from ad_marketplace import get_all_agencies, get_agency_by_id
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    question: str
    newspaper: str = None

class FeedbackRequest(BaseModel):
    rating: int
    feature_used: str
    comment: str = None

class RegisterRequest(BaseModel):
    name: str
    email: str

@app.on_event("startup")
def startup():
    start_scheduler()

@app.get("/")
def home():
    return {"message": "Welcome to NewsBot API", "status": "running"}

@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.fetched_at.desc()).limit(50).all()
    return {
        "articles": [
            {
                "id": a.id,
                "newspaper": a.newspaper_name,
                "title": a.title,
                "description": a.description,
                "published_at": str(a.published_at),
                "url": a.url,
                "image_url": a.image_url or ""
            }
            for a in articles
        ],
        "total": len(articles)
    }

@app.get("/articles/{newspaper_name}")
def get_newspaper_articles(newspaper_name: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(
        Article.newspaper_name == newspaper_name
    ).order_by(Article.fetched_at.desc()).limit(20).all()
    return {
        "articles": [
            {
                "id": a.id,
                "newspaper": a.newspaper_name,
                "title": a.title,
                "description": a.description,
                "published_at": str(a.published_at),
                "url": a.url,
                "image_url": a.image_url or ""
            }
            for a in articles
        ],
        "newspaper": newspaper_name
    }

@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    result = answer_question(request.question)
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "status": "success"
    }

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(
        Alert.is_read == False
    ).order_by(Alert.created_at.desc()).all()
    return {
        "alerts": [
            {
                "id": a.id,
                "message": a.message,
                "created_at": str(a.created_at)
            }
            for a in alerts
        ]
    }

@app.put("/alerts/{alert_id}/read")
def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.is_read = True
        db.commit()
    return {"message": "Alert marked as read"}

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    feedback = Feedback(
        rating=request.rating,
        feature_used=request.feature_used,
        comment=request.comment
    )
    db.add(feedback)
    db.commit()
    return {"message": "Thank you for your feedback!", "status": "success"}

@app.post("/fetch-now")
def fetch_now():
    fetch_and_store()
    return {"message": "Newspapers fetched successfully", "status": "success"}

@app.get("/archive")
def search_archive(
    keyword: str = None,
    date_from: str = None,
    date_to: str = None,
    newspaper: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    if keyword:
        query = query.filter(
            (Article.title.like(f"%{keyword}%")) |
            (Article.content.like(f"%{keyword}%")) |
            (Article.description.like(f"%{keyword}%"))
        )
    if newspaper and newspaper != "All":
        query = query.filter(Article.newspaper_name == newspaper)
    if date_from:
        query = query.filter(Article.published_at >= date_from)
    if date_to:
        query = query.filter(Article.published_at <= date_to)
    articles = query.order_by(Article.fetched_at.desc()).limit(50).all()
    return {
        "articles": [
            {
                "id": a.id,
                "newspaper": a.newspaper_name,
                "title": a.title,
                "description": a.description,
                "published_at": str(a.published_at),
                "url": a.url,
                "image_url": a.image_url or ""
            }
            for a in articles
        ],
        "total": len(articles)
    }

@app.get("/compare")
def compare_newspapers(topic: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(
        (Article.title.like(f"%{topic}%")) |
        (Article.content.like(f"%{topic}%")) |
        (Article.description.like(f"%{topic}%"))
    ).order_by(Article.fetched_at.desc()).limit(30).all()
    grouped = {}
    for a in articles:
        if a.newspaper_name not in grouped:
            grouped[a.newspaper_name] = []
        grouped[a.newspaper_name].append({
            "title": a.title,
            "description": a.description,
            "published_at": str(a.published_at),
            "url": a.url,
            "image_url": a.image_url or ""
        })
    return {"topic": topic, "comparison": grouped}

@app.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        return {"message": "Already registered", "status": "exists"}
    new_user = User(
        name=request.name,
        email=request.email,
        preferred_newspapers="All"
    )
    db.add(new_user)
    db.commit()
    return {"message": "Registered successfully!", "status": "success"}

@app.get("/newspapers")
def get_newspapers_list(db: Session = Depends(get_db)):
    results = db.query(Article.newspaper_name).distinct().all()
    return {"newspapers": [r[0] for r in results]}

@app.get("/analytics")
def get_analytics_data():
    data = get_analytics()
    return data

# ============ V4 ROUTES ============

@app.get("/agencies")
def get_agencies(
    newspaper: str = None,
    max_budget: int = None,
    specialization: str = None
):
    agencies = get_all_agencies(newspaper, max_budget, specialization)
    return {"agencies": agencies, "total": len(agencies)}

@app.get("/agencies/{agency_id}")
def get_agency(agency_id: int):
    agency = get_agency_by_id(agency_id)
    if not agency:
        return {"error": "Agency not found"}
    return agency
    