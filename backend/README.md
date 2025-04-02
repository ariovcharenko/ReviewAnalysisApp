# Review Analysis API

This is the backend API for the Sentiment & Aspect-Based Review Analysis Web App. It provides endpoints for analyzing product reviews, extracting key aspects, and detecting sentiment.

## Features

- Sentiment analysis using BERT
- Aspect-based sentiment analysis using SpaCy and BERT
- Review summarization using T5
- SQLite database for storing reviews and analysis results (no database server required)
- RESTful API with FastAPI

## Requirements

- Python 3.9+
- Docker (optional)

## Setup

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install SpaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Run the application:
   ```bash
   python run.py
   ```

   The SQLite database file will be created automatically at `review_analysis.db`

5. Access the API documentation at http://localhost:8000/docs

### Docker

1. Build the Docker image:
   ```bash
   docker build -t review-analysis-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env review-analysis-api
   ```

## API Endpoints

### Reviews

- `POST /api/reviews/`: Create a new review
- `GET /api/reviews/`: Get all reviews
- `GET /api/reviews/{review_id}`: Get a specific review
- `POST /api/reviews/upload-csv`: Upload and process a CSV file of reviews
- `DELETE /api/reviews/{review_id}`: Delete a review
- `GET /api/reviews/{review_id}/full-analysis`: Get a review with its analysis

### Sentiment Analysis

- `POST /api/sentiment/analyze`: Analyze sentiment of a text
- `POST /api/sentiment/analyze-review/{review_id}`: Analyze sentiment of a review
- `POST /api/sentiment/analyze-batch`: Analyze sentiment for multiple reviews
- `GET /api/sentiment/trends`: Get sentiment trends over time

### Aspect Extraction

- `POST /api/aspects/extract`: Extract aspects from text
- `POST /api/aspects/analyze-review/{review_id}`: Extract aspects from a review
- `POST /api/aspects/analyze-batch`: Extract aspects for multiple reviews
- `GET /api/aspects/top`: Get top aspects mentioned across all reviews

### Summarization

- `POST /api/summarization/summarize`: Generate a summary for a text
- `POST /api/summarization/summarize-review/{review_id}`: Generate a summary for a review
- `POST /api/summarization/summarize-batch`: Generate summaries for multiple reviews
- `GET /api/summarization/review/{review_id}`: Get the summary for a specific review

## Deployment

The API can be deployed to AWS Lambda or EC2 using the provided Dockerfile.
