from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import io
import pandas as pd

from app.database.database import get_db
from app.models import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review"""
    db_review = models.Review(
        text=review.text,
        rating=review.rating,
        source=review.source
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/", response_model=List[schemas.ReviewResponse])
def get_reviews(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get all reviews with pagination"""
    reviews = db.query(models.Review).offset(skip).limit(limit).all()
    return reviews

@router.get("/{review_id}", response_model=schemas.ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review by ID"""
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/upload-csv", response_model=schemas.FileUploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a CSV file of reviews"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )
    
    # Read CSV file
    contents = await file.read()
    
    try:
        # Parse CSV
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Check required columns
        if 'text' not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain a 'text' column"
            )
        
        # Process reviews
        reviews_processed = 0
        for _, row in df.iterrows():
            # Get review text (required)
            text = row['text']
            
            # Get rating if available
            rating = None
            if 'rating' in df.columns and not pd.isna(row['rating']):
                rating = float(row['rating'])
            
            # Create review
            db_review = models.Review(
                text=text,
                rating=rating,
                source="csv"
            )
            db.add(db_review)
            reviews_processed += 1
        
        # Commit all reviews to database
        db.commit()
        
        return {
            "filename": file.filename,
            "reviews_processed": reviews_processed,
            "success": True
        }
    
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing CSV file: {str(e)}"
        )

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """Delete a review by ID"""
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Delete related records
    db.query(models.SentimentAnalysis).filter(models.SentimentAnalysis.review_id == review_id).delete()
    db.query(models.AspectAnalysis).filter(models.AspectAnalysis.review_id == review_id).delete()
    db.query(models.ReviewSummary).filter(models.ReviewSummary.review_id == review_id).delete()
    
    # Delete review
    db.delete(review)
    db.commit()
    
    return None

@router.get("/{review_id}/full-analysis", response_model=schemas.ReviewAnalysisResponse)
def get_review_with_analysis(review_id: int, db: Session = Depends(get_db)):
    """Get a review with its sentiment analysis, aspect analysis, and summary"""
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {
        "review": review,
        "sentiment": review.sentiment_analysis,
        "aspects": review.aspect_analyses,
        "summary": review.summary
    }
