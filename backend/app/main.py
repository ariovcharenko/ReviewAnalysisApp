from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database import engine, Base
from app.routers import reviews, sentiment, aspects, summarization
from app.database.database import get_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Review Analysis API",
    description="API for sentiment and aspect-based review analysis",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js frontend
    "https://review-analysis-frontend.vercel.app",  # Production frontend
    "null",  # Allow requests from file:// protocol
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(sentiment.router, prefix="/api/sentiment", tags=["Sentiment Analysis"])
app.include_router(aspects.router, prefix="/api/aspects", tags=["Aspect Extraction"])
app.include_router(summarization.router, prefix="/api/summarization", tags=["Summarization"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Review Analysis API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
