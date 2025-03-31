# Sentiment & Aspect-Based Review Analysis Web App

A comprehensive web application for analyzing product reviews semantically, extracting key aspects (battery, camera, design, etc.), and detecting sentiment (positive, neutral, negative).

## 🌟 Features

### 🔹 User Interface
- Clean UI for inputting or uploading product reviews
- Text box for manual review input
- File upload option for bulk reviews (CSV format)
- Results section displaying:
  - Overall Sentiment (Positive, Neutral, Negative)
  - Key Aspects with detected sentiment
  - Summarized Review (AI-generated summary)
- Trend graph showing sentiment changes over time
- Table listing uploaded reviews with filter options

### 🔹 Backend Capabilities
- Text preprocessing (tokenization, stopword removal)
- Sentiment analysis using a fine-tuned BERT model
- Aspect extraction using SpaCy
- Aspect sentiment detection
- Review summarization using T5 model
- Fake review detection (checking sentiment mismatch with rating)
- PostgreSQL database for storing reviews and analysis results

## 🛠️ Tech Stack

### Frontend
- React (Next.js)
- Tailwind CSS
- Chart.js for data visualization
- Axios for API requests

### Backend
- FastAPI (Python)
- Hugging Face Transformers (BERT, T5)
- SpaCy for NLP tasks
- SQLAlchemy for database ORM
- PostgreSQL for data storage

### Deployment
- Docker for containerization
- AWS Lambda/EC2 for backend deployment
- Vercel for frontend deployment

## 📋 Project Structure

```
ReviewAnalysisApp/
├── backend/               # FastAPI backend
│   ├── app/               # Application code
│   │   ├── database/      # Database configuration
│   │   ├── models/        # Database models and schemas
│   │   ├── routers/       # API endpoints
│   │   └── services/      # NLP services
│   ├── Dockerfile         # Backend Docker configuration
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # Next.js frontend
│   ├── app/               # Next.js app directory
│   │   ├── analyze/       # Review analysis pages
│   │   ├── dashboard/     # Dashboard page
│   │   └── reviews/       # Reviews listing page
│   └── package.json       # Node.js dependencies
│
└── docker/                # Docker compose configuration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker (optional)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd ReviewAnalysisApp/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install SpaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Run the application:
   ```bash
   python run.py
   ```

   The SQLite database file will be created automatically at `review_analysis.db`

6. Access the API documentation at http://localhost:8000/docs

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ReviewAnalysisApp/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

### Docker Setup (Optional)

1. Build and run the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the application at http://localhost:3000

## 📊 Usage Examples

1. **Single Review Analysis**:
   - Enter a product review in the text box
   - Click "Analyze Review"
   - View the sentiment analysis, aspect extraction, and summary

2. **Bulk Review Analysis**:
   - Prepare a CSV file with a 'text' column containing reviews
   - Upload the CSV file
   - View the analysis results in the dashboard

3. **Trend Analysis**:
   - Navigate to the Dashboard
   - View sentiment trends over time
   - Identify top aspects mentioned in reviews

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
