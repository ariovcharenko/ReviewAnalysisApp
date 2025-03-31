from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Review Schemas
class ReviewBase(BaseModel):
    text: str
    rating: Optional[float] = None
    source: Optional[str] = "manual"

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Sentiment Analysis Schemas
class SentimentAnalysisBase(BaseModel):
    sentiment_score: float
    sentiment_label: str
    confidence: float

class SentimentAnalysisCreate(SentimentAnalysisBase):
    review_id: int

class SentimentAnalysisResponse(SentimentAnalysisBase):
    id: int
    review_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Aspect Analysis Schemas
class AspectAnalysisBase(BaseModel):
    aspect: str
    sentiment_score: float
    sentiment_label: str
    confidence: float
    relevant_text: Optional[str] = None

class AspectAnalysisCreate(AspectAnalysisBase):
    review_id: int

class AspectAnalysisResponse(AspectAnalysisBase):
    id: int
    review_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Review Summary Schemas
class ReviewSummaryBase(BaseModel):
    summary_text: str

class ReviewSummaryCreate(ReviewSummaryBase):
    review_id: int

class ReviewSummaryResponse(ReviewSummaryBase):
    id: int
    review_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Review Trend Schemas
class ReviewTrendBase(BaseModel):
    date: datetime
    total_reviews: int
    avg_sentiment: float
    sentiment_distribution: Dict[str, int]
    top_aspects: List[Dict[str, Any]]

class ReviewTrendCreate(ReviewTrendBase):
    pass

class ReviewTrendResponse(ReviewTrendBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Combined Response Schemas
class ReviewAnalysisResponse(BaseModel):
    review: ReviewResponse
    sentiment: Optional[SentimentAnalysisResponse] = None
    aspects: List[AspectAnalysisResponse] = []
    summary: Optional[ReviewSummaryResponse] = None

# Request Schemas
class TextAnalysisRequest(BaseModel):
    text: str

class FileUploadResponse(BaseModel):
    filename: str
    reviews_processed: int
    success: bool

class AnalysisRequest(BaseModel):
    review_id: int

class BulkAnalysisRequest(BaseModel):
    review_ids: List[int]
