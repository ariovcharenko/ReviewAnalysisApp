from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.database import get_db
from app.models import models, schemas
from app.services.summarization_service import summarization_service

router = APIRouter()

@router.post("/summarize", response_model=Dict[str, str])
def summarize_text(request: schemas.TextAnalysisRequest):
    """Generate a summary for a text without storing in database"""
    try:
        summary = summarization_service.generate_summary(request.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {str(e)}"
        )

@router.post("/summarize-review/{review_id}", response_model=schemas.ReviewSummaryResponse)
def summarize_review(review_id: int, db: Session = Depends(get_db)):
    """Generate a summary for a review and store the result"""
    # Get review
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    try:
        # Generate summary
        summary_text = summarization_service.generate_summary(review.text)
        
        # Check if summary already exists
        existing_summary = db.query(models.ReviewSummary).filter(
            models.ReviewSummary.review_id == review_id
        ).first()
        
        if existing_summary:
            # Update existing summary
            existing_summary.summary_text = summary_text
            db_summary = existing_summary
        else:
            # Create new summary
            db_summary = models.ReviewSummary(
                review_id=review_id,
                summary_text=summary_text
            )
            db.add(db_summary)
        
        # Commit changes
        db.commit()
        db.refresh(db_summary)
        
        return db_summary
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {str(e)}"
        )

@router.post("/summarize-batch", response_model=Dict[str, str])
def summarize_batch(request: schemas.BulkAnalysisRequest, db: Session = Depends(get_db)):
    """Generate summaries for multiple reviews"""
    # Get reviews
    reviews = db.query(models.Review).filter(models.Review.id.in_(request.review_ids)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    
    try:
        results = {}
        
        for review in reviews:
            # Generate summary
            summary_text = summarization_service.generate_summary(review.text)
            
            # Check if summary already exists
            existing_summary = db.query(models.ReviewSummary).filter(
                models.ReviewSummary.review_id == review.id
            ).first()
            
            if existing_summary:
                # Update existing summary
                existing_summary.summary_text = summary_text
            else:
                # Create new summary
                db_summary = models.ReviewSummary(
                    review_id=review.id,
                    summary_text=summary_text
                )
                db.add(db_summary)
            
            # Store result
            results[str(review.id)] = summary_text
        
        # Commit changes
        db.commit()
        
        return results
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summaries: {str(e)}"
        )

@router.get("/review/{review_id}", response_model=schemas.ReviewSummaryResponse)
def get_review_summary(review_id: int, db: Session = Depends(get_db)):
    """Get the summary for a specific review"""
    summary = db.query(models.ReviewSummary).filter(
        models.ReviewSummary.review_id == review_id
    ).first()
    
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    return summary
