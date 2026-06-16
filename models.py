from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Newspaper(Base):
    __tablename__ = "newspapers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    source_type = Column(String(50))
    feed_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    newspaper_id = Column(Integer)
    newspaper_name = Column(String(255))
    title = Column(String(500))
    description = Column(Text)
    content = Column(Text)
    published_at = Column(String(100))
    url = Column(String(500))
    image_url = Column(String(500))
    fetched_at = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    preferred_newspapers = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(500))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    feature_used = Column(String(255))
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    