from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import os
import json

# Create the app
app = FastAPI(
    title="Simple Review Analysis API",
    description="Simplified API for review management",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js frontend
    "https://review-analysis-frontend.vercel.app",  # Production frontend
    "null",  # Allow requests from file:// protocol
    "*",  # Allow all origins (for testing only)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class ReviewCreate(BaseModel):
    text: str
    rating: Optional[float] = None
    source: Optional[str] = "manual"

class ReviewResponse(BaseModel):
    id: int
    text: str
    rating: Optional[float] = None
    source: Optional[str] = "manual"
    created_at: str

# Database setup
DB_PATH = "simple_reviews.db"

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        rating REAL,
        source TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# API routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple Review Analysis API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate):
    """Create a new review"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert review into database
    cursor.execute(
        "INSERT INTO reviews (text, rating, source) VALUES (?, ?, ?)",
        (review.text, review.rating, review.source)
    )
    conn.commit()
    
    # Get the inserted review
    review_id = cursor.lastrowid
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "text": row[1],
            "rating": row[2],
            "source": row[3],
            "created_at": row[4]
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to create review")

@app.get("/api/reviews", response_model=List[ReviewResponse])
def get_reviews(skip: int = 0, limit: int = 100):
    """Get all reviews with pagination"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    
    reviews = []
    for row in rows:
        reviews.append({
            "id": row[0],
            "text": row[1],
            "rating": row[2],
            "source": row[3],
            "created_at": row[4]
        })
    
    return reviews

@app.get("/api/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int):
    """Get a specific review by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "text": row[1],
            "rating": row[2],
            "source": row[3],
            "created_at": row[4]
        }
    else:
        raise HTTPException(status_code=404, detail="Review not found")

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: int):
    """Delete a review by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM reviews WHERE id = ?", (review_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Review not found")
    
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Review deleted successfully"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple-backend:app", host="0.0.0.0", port=8000, reload=True)
