from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.database import get_db
from app.models import models, schemas
from app.services.sentiment_service import sentiment_service

router = APIRouter()

@router.post("/analyze", response_model=Dict[str, Any])
def analyze_text(request: schemas.TextAnalysisRequest):
    """Analyze sentiment of a text without storing in database"""
    try:
        result = sentiment_service.analyze_sentiment(request.text)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        )

@router.post("/analyze-review/{review_id}", response_model=schemas.SentimentAnalysisResponse)
def analyze_review(review_id: int, db: Session = Depends(get_db)):
    """Analyze sentiment of a review and store the result"""
    # Get review
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    try:
        # Analyze sentiment
        result = sentiment_service.analyze_sentiment(review.text)
        
        # Check if sentiment analysis already exists for this review
        existing_analysis = db.query(models.SentimentAnalysis).filter(
            models.SentimentAnalysis.review_id == review_id
        ).first()
        
        if existing_analysis:
            # Update existing analysis
            existing_analysis.sentiment_score = result["sentiment_score"]
            existing_analysis.sentiment_label = result["sentiment_label"]
            existing_analysis.confidence = result["confidence"]
            db_analysis = existing_analysis
        else:
            # Create new sentiment analysis
            db_analysis = models.SentimentAnalysis(
                review_id=review_id,
                sentiment_score=result["sentiment_score"],
                sentiment_label=result["sentiment_label"],
                confidence=result["confidence"]
            )
            db.add(db_analysis)
        
        # Commit changes
        db.commit()
        db.refresh(db_analysis)
        
        return db_analysis
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        )

@router.post("/analyze-batch", response_model=List[Dict[str, Any]])
def analyze_batch(request: schemas.BulkAnalysisRequest, db: Session = Depends(get_db)):
    """Analyze sentiment for multiple reviews"""
    # Get reviews
    reviews = db.query(models.Review).filter(models.Review.id.in_(request.review_ids)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    
    try:
        # Extract texts
        texts = [review.text for review in reviews]
        
        # Analyze sentiment
        results = sentiment_service.analyze_batch(texts)
        
        # Store results in database
        for i, review in enumerate(reviews):
            result = results[i]
            
            # Check if sentiment analysis already exists
            existing_analysis = db.query(models.SentimentAnalysis).filter(
                models.SentimentAnalysis.review_id == review.id
            ).first()
            
            if existing_analysis:
                # Update existing analysis
                existing_analysis.sentiment_score = result["sentiment_score"]
                existing_analysis.sentiment_label = result["sentiment_label"]
                existing_analysis.confidence = result["confidence"]
            else:
                # Create new sentiment analysis
                db_analysis = models.SentimentAnalysis(
                    review_id=review.id,
                    sentiment_score=result["sentiment_score"],
                    sentiment_label=result["sentiment_label"],
                    confidence=result["confidence"]
                )
                db.add(db_analysis)
        
        # Commit changes
        db.commit()
        
        # Return results
        return results
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        )

@router.get("/trends", response_model=List[schemas.ReviewTrendResponse])
def get_sentiment_trends(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get sentiment trends over time"""
    trends = db.query(models.ReviewTrend).order_by(models.ReviewTrend.date.desc()).limit(limit).all()
    return trends
