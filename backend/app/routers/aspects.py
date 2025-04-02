from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.database import get_db
from app.models import models, schemas
from app.services.aspect_service import aspect_service

router = APIRouter()

@router.post("/extract", response_model=List[Dict[str, Any]])
def extract_aspects(request: schemas.TextAnalysisRequest):
    """Extract aspects from text and analyze their sentiment without storing in database"""
    try:
        result = aspect_service.extract_aspects(request.text)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting aspects: {str(e)}"
        )

@router.post("/analyze-review/{review_id}", response_model=List[schemas.AspectAnalysisResponse])
def analyze_review_aspects(review_id: int, db: Session = Depends(get_db)):
    """Extract aspects from a review and store the results"""
    # Get review
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    try:
        # Extract aspects
        aspects = aspect_service.extract_aspects(review.text)
        
        # Delete existing aspect analyses for this review
        db.query(models.AspectAnalysis).filter(
            models.AspectAnalysis.review_id == review_id
        ).delete()
        
        # Create new aspect analyses
        db_aspects = []
        for aspect in aspects:
            db_aspect = models.AspectAnalysis(
                review_id=review_id,
                aspect=aspect["aspect"],
                sentiment_score=aspect["sentiment_score"],
                sentiment_label=aspect["sentiment_label"],
                confidence=aspect["confidence"],
                relevant_text=aspect["relevant_text"]
            )
            db.add(db_aspect)
            db_aspects.append(db_aspect)
        
        # Commit changes
        db.commit()
        
        # Refresh all aspect analyses
        for db_aspect in db_aspects:
            db.refresh(db_aspect)
        
        return db_aspects
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing aspects: {str(e)}"
        )

@router.post("/analyze-batch", response_model=Dict[str, List[Dict[str, Any]]])
def analyze_batch_aspects(request: schemas.BulkAnalysisRequest, db: Session = Depends(get_db)):
    """Extract aspects for multiple reviews"""
    # Get reviews
    reviews = db.query(models.Review).filter(models.Review.id.in_(request.review_ids)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    
    try:
        results = {}
        
        for review in reviews:
            # Extract aspects
            aspects = aspect_service.extract_aspects(review.text)
            
            # Delete existing aspect analyses
            db.query(models.AspectAnalysis).filter(
                models.AspectAnalysis.review_id == review.id
            ).delete()
            
            # Create new aspect analyses
            for aspect in aspects:
                db_aspect = models.AspectAnalysis(
                    review_id=review.id,
                    aspect=aspect["aspect"],
                    sentiment_score=aspect["sentiment_score"],
                    sentiment_label=aspect["sentiment_label"],
                    confidence=aspect["confidence"],
                    relevant_text=aspect["relevant_text"]
                )
                db.add(db_aspect)
            
            # Store results
            results[str(review.id)] = aspects
        
        # Commit changes
        db.commit()
        
        return results
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing aspects: {str(e)}"
        )

@router.get("/top", response_model=List[Dict[str, Any]])
def get_top_aspects(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get top aspects mentioned across all reviews"""
    # This is a more complex query that would typically use raw SQL or ORM aggregation
    # For simplicity, we'll use a basic approach here
    
    # Get all aspect analyses
    aspect_analyses = db.query(models.AspectAnalysis).all()
    
    # Count occurrences of each aspect
    aspect_counts = {}
    aspect_sentiments = {}
    
    for analysis in aspect_analyses:
        aspect = analysis.aspect
        
        # Count occurrences
        if aspect in aspect_counts:
            aspect_counts[aspect] += 1
            aspect_sentiments[aspect].append(analysis.sentiment_score)
        else:
            aspect_counts[aspect] = 1
            aspect_sentiments[aspect] = [analysis.sentiment_score]
    
    # Calculate average sentiment for each aspect
    results = []
    for aspect, count in aspect_counts.items():
        avg_sentiment = sum(aspect_sentiments[aspect]) / len(aspect_sentiments[aspect])
        
        # Determine sentiment label
        if avg_sentiment > 0.3:
            sentiment_label = "positive"
        elif avg_sentiment < -0.3:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        results.append({
            "aspect": aspect,
            "count": count,
            "avg_sentiment": avg_sentiment,
            "sentiment_label": sentiment_label
        })
    
    # Sort by count (descending)
    results.sort(key=lambda x: x["count"], reverse=True)
    
    # Limit results
    return results[:limit]
