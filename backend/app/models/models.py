from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base

class Review(Base):
    """Model for storing user-submitted reviews"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    rating = Column(Float, nullable=True)  # Optional user-provided rating
    source = Column(String(255), nullable=True)  # Source of the review (e.g., "manual", "csv")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="review", uselist=False)
    aspect_analyses = relationship("AspectAnalysis", back_populates="review")
    summary = relationship("ReviewSummary", back_populates="review", uselist=False)

class SentimentAnalysis(Base):
    """Model for storing sentiment analysis results"""
    __tablename__ = "sentiment_analyses"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    sentiment_score = Column(Float, nullable=False)  # Range from -1 (negative) to 1 (positive)
    sentiment_label = Column(String(50), nullable=False)  # "positive", "neutral", "negative"
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    review = relationship("Review", back_populates="sentiment_analysis")

class AspectAnalysis(Base):
    """Model for storing aspect-based sentiment analysis results"""
    __tablename__ = "aspect_analyses"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    aspect = Column(String(255), nullable=False)  # e.g., "battery", "camera", "design"
    sentiment_score = Column(Float, nullable=False)
    sentiment_label = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    relevant_text = Column(Text, nullable=True)  # The specific text mentioning this aspect
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    review = relationship("Review", back_populates="aspect_analyses")

class ReviewSummary(Base):
    """Model for storing AI-generated review summaries"""
    __tablename__ = "review_summaries"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    summary_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    review = relationship("Review", back_populates="summary")

class ReviewTrend(Base):
    """Model for storing historical review trends"""
    __tablename__ = "review_trends"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    total_reviews = Column(Integer, nullable=False)
    avg_sentiment = Column(Float, nullable=False)
    sentiment_distribution = Column(JSON, nullable=False)  # {"positive": 10, "neutral": 5, "negative": 2}
    top_aspects = Column(JSON, nullable=False)  # [{"aspect": "battery", "count": 5, "avg_sentiment": 0.8}, ...]
    created_at = Column(DateTime, default=datetime.utcnow)
