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

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, etc.)
- Git Bash (for Windows users)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/ariovcharenko/ReviewAnalysisApp.git
   cd ReviewAnalysisApp
   ```

## Frontend Setup

There are two ways to run the frontend:

### Option 1: Using a Local Web Server (Recommended)

This method is recommended as it ensures proper functionality of the application.

1. Open Git Bash or your terminal and navigate to the ReviewAnalysisApp directory:
   ```bash
   cd /path/to/ReviewAnalysisApp
   ```

2. Start a local web server:
   ```bash
   python -m http.server 8080
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8080/simple-frontend.html
   ```

### Option 2: Opening the HTML File Directly

**Note**: This method may not work properly due to browser security restrictions when making API calls.

1. Right-click on `simple-frontend.html` in your file explorer
2. Select "Open with" and choose your preferred browser

If you see only raw HTML or the page doesn't function correctly, please use Option 1 instead.

## Backend Setup

There are two backend options available:

### Option 1: Simple Backend (Recommended for Beginners)

1. Open Git Bash or your terminal and navigate to the ReviewAnalysisApp directory:
   ```bash
   cd /path/to/ReviewAnalysisApp
   ```

2. Create a Python virtual environment:
   ```bash
   # For Windows (Git Bash)
   python -m venv venv
   source venv/Scripts/activate
   
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install fastapi uvicorn pydantic sqlite3
   ```

4. Run the simple backend:
   ```bash
   python simple-backend.py
   ```
   
   The backend will run on http://localhost:8000

### Option 2: Full-Featured Backend

1. Open Git Bash or your terminal and navigate to the backend directory:
   ```bash
   cd /path/to/ReviewAnalysisApp/backend
   ```

2. Create a Python virtual environment:
   ```bash
   # For Windows (Git Bash)
   python -m venv venv
   source venv/Scripts/activate
   
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Run the backend:
   ```bash
   python run.py
   ```
   
   The backend will run on http://localhost:8000

## Connecting Frontend to Backend

By default, the frontend is configured to connect to a backend at http://localhost:3000/api, but our Python backend runs on port 8000. You need to modify the frontend to connect to the correct port:

1. Open `simple-frontend.html` in a text editor
2. Find the line that says:
   ```javascript
   const API_URL = 'http://localhost:3000/api';
   ```
3. Change it to:
   ```javascript
   const API_URL = 'http://localhost:8000/api';
   ```
4. Save the file and refresh your browser

## Troubleshooting

### Frontend Issues

1. **Page shows only raw HTML code**:
   - Make sure you're using a local web server (Option 1 in Frontend Setup)
   - Check that you're accessing the correct URL (http://localhost:8080/simple-frontend.html)

2. **Cannot connect to backend**:
   - Ensure the backend is running (check terminal for any error messages)
   - Verify that the API_URL in simple-frontend.html matches your backend port
   - Check browser console (F12) for any error messages

### Backend Issues

1. **Virtual environment creates in wrong location**:
   - If using Git Bash on Windows and venv creates in C:\Program Files\Git\venv:
     - Use the full path: `python -m venv /c/Users/YourUsername/path/to/ReviewAnalysisApp/venv`
     - Or use Windows Command Prompt instead of Git Bash

2. **Activation script not found**:
   - Ensure you're using the correct path:
     - Windows: `source venv/Scripts/activate`
     - macOS/Linux: `source venv/bin/activate`

3. **spaCy installation errors**:
   - Try installing with: `pip install spacy==3.7.2`
   - Then download the language model: `python -m spacy download en_core_web_sm`

4. **Permission errors when running scripts**:
   - Ensure you have the necessary permissions to execute the files
   - Try running with elevated privileges if necessary

## Port Usage

- **Frontend**: Served on port 8080 using Python's built-in HTTP server
- **Backend**: Runs on port 8000 using Uvicorn (FastAPI)

The frontend communicates with the backend by making API requests to http://localhost:8000/api endpoints.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
