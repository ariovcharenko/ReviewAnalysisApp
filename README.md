# Review Analysis App

A web application for analyzing product reviews with sentiment analysis and aspect-based feedback detection.

## Features

- **Star Rating Input**: Interactive 5-star rating system for review submission
- **Aspect-Based Sentiment Analysis**: Detects and analyzes sentiment for specific product aspects like:
  - Battery life
  - Screen quality
  - Camera quality
  - Performance
  - Sound quality
  - Charging speed
  - Overheating
  - And many more
- **Detailed Review Analysis**: View comprehensive analysis of each review
- **File Upload**: Support for batch processing of reviews via file upload
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js (for the backend server)
- Modern web browser

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/ariovcharenko/ReviewAnalysisApp.git
   cd ReviewAnalysisApp
   ```

2. Start the backend server:
   ```
   cd backend
   npm install
   npm start
   ```
   The backend server will run on http://localhost:3000

3. Open the frontend:
   - You can simply open `simple-frontend.html` in your browser
   - Or serve it using a local server:
     ```
     cd ..
     python -m http.server 8080
     ```
     Then visit http://localhost:8080/simple-frontend.html

## Usage

### Adding a Review

1. Enter your review text in the text area
2. Select a star rating (1-5 stars)
3. Click "Submit Review"

### Uploading Reviews in Batch

1. Prepare a CSV or TXT file with your reviews
2. Click "Choose File" and select your file
3. Click "Upload and Analyze"
4. Wait for the success message

### Viewing Review Analysis

1. All reviews are displayed in the "Reviews" section
2. Click "View Full Details" on any review to see:
   - Overall sentiment analysis
   - Aspect-based sentiment breakdown
   - Complete review text and rating

## Implementation Details

### Frontend

- Pure HTML, CSS, and JavaScript
- No external libraries or frameworks
- Responsive design for all device sizes

### Backend

- RESTful API for review management
- Sentiment analysis using natural language processing
- Aspect extraction for detailed product feedback

## License

This project is licensed under the MIT License - see the LICENSE file for details.
