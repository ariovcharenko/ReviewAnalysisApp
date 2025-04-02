# Review Analysis App - Comprehensive Installation Guide

This guide provides detailed, step-by-step instructions for setting up and running the Review Analysis App on Windows using Git Bash.

## Prerequisites

- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/downloads/)
- **Git Bash**: Download from [git-scm.com](https://git-scm.com/downloads)
- **Modern web browser**: Chrome, Firefox, Edge, etc.

## Step 1: Clone the Repository

1. Open Git Bash
2. Navigate to where you want to install the application
3. Clone the repository:
   ```bash
   git clone https://github.com/ariovcharenko/ReviewAnalysisApp.git
   cd ReviewAnalysisApp
   ```

## Step 2: Set Up the Backend

You can choose between two backend options:

### Option A: Simple Backend (Recommended for Beginners)

1. Open Git Bash and navigate to the ReviewAnalysisApp directory:
   ```bash
   cd /path/to/ReviewAnalysisApp
   ```

2. Create a Python virtual environment:
   ```bash
   # Use absolute path to avoid Git Bash path issues
   python -m venv /c/Users/YourUsername/path/to/ReviewAnalysisApp/venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/Scripts/activate
   ```
   
   You should see `(venv)` at the beginning of your command prompt.

4. Install the required packages:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

5. Run the simple backend:
   ```bash
   python simple-backend.py
   ```
   
   You should see output indicating that the server is running on http://localhost:8000.

### Option B: Full-Featured Backend

1. Open Git Bash and navigate to the backend directory:
   ```bash
   cd /path/to/ReviewAnalysisApp/backend
   ```

2. Create a Python virtual environment:
   ```bash
   # Use absolute path to avoid Git Bash path issues
   python -m venv /c/Users/YourUsername/path/to/ReviewAnalysisApp/backend/venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/Scripts/activate
   ```
   
   You should see `(venv)` at the beginning of your command prompt.

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   This may take a few minutes as it installs several machine learning libraries.

5. Install the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. Run the backend:
   ```bash
   python run.py
   ```
   
   You should see output indicating that the server is running on http://localhost:8000.

## Step 3: Configure the Frontend

The frontend needs to be configured to connect to the correct backend port:

1. Open `simple-frontend.html` in a text editor
2. Find the line that says:
   ```javascript
   const API_URL = 'http://localhost:3000/api';
   ```
3. Change it to:
   ```javascript
   const API_URL = 'http://localhost:8000/api';
   ```
4. Save the file

## Step 4: Run the Frontend

There are two ways to run the frontend:

### Option A: Using a Local Web Server (Recommended)

1. Open a new Git Bash window (keep the backend running in the first window)
2. Navigate to the ReviewAnalysisApp directory:
   ```bash
   cd /path/to/ReviewAnalysisApp
   ```

3. Start a local web server:
   ```bash
   python -m http.server 8080
   ```
   
   You should see output indicating that the server is running on port 8080.

4. Open your browser and navigate to:
   ```
   http://localhost:8080/simple-frontend.html
   ```

### Option B: Opening the HTML File Directly

**Note**: This method may not work properly due to browser security restrictions.

1. Open File Explorer and navigate to the ReviewAnalysisApp directory
2. Right-click on `simple-frontend.html`
3. Select "Open with" and choose your preferred browser

If you see only raw HTML or the page doesn't function correctly, please use Option A instead.

## Step 5: Verify the Installation

1. Ensure both the backend and frontend servers are running
2. In your browser, navigate to http://localhost:8080/simple-frontend.html
3. You should see the Review Analysis App interface
4. Try adding a review:
   - Enter some text in the review text area
   - Select a star rating
   - Click "Submit Review"
5. The review should appear in the "Reviews" section
6. Click "View Full Details" on the review to see the sentiment analysis

## Troubleshooting

If you encounter any issues during installation or setup, please refer to the `TROUBLESHOOTING.md` file for detailed solutions to common problems.

## Port Usage Summary

- **Backend**: Runs on port 8000 (Python/FastAPI)
- **Frontend**: Served on port 8080 (Python's http.server)

The frontend makes API requests to the backend at http://localhost:8000/api.
