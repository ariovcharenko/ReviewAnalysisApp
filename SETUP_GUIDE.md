# Review Analysis App - Quick Setup Guide

This guide provides step-by-step instructions for setting up and running the Review Analysis App on Windows using Git Bash.

## Frontend Setup

### Option 1: Using a Local Web Server (Recommended)

1. Open Git Bash and navigate to the ReviewAnalysisApp directory:
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

## Backend Setup

### Option 1: Simple Backend (Recommended for Beginners)

1. Open a new Git Bash window and navigate to the ReviewAnalysisApp directory:
   ```bash
   cd /path/to/ReviewAnalysisApp
   ```

2. Create a Python virtual environment:
   ```bash
   # Use absolute path to avoid Git Bash path issues
   python -m venv /c/Users/YourUsername/path/to/ReviewAnalysisApp/venv
   source venv/Scripts/activate
   ```

3. Install the required packages:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

4. Run the simple backend:
   ```bash
   python simple-backend.py
   ```

## Troubleshooting

### Frontend Issues

- **Problem**: Page shows only raw HTML code
  - **Solution**: Make sure you're using a local web server (Option 1 in Frontend Setup)

- **Problem**: Cannot connect to backend
  - **Solution**: Ensure the backend is running and check browser console (F12) for error messages

### Backend Issues

- **Problem**: Virtual environment creates in wrong location
  - **Solution**: Use the full path: `python -m venv /c/Users/YourUsername/path/to/ReviewAnalysisApp/venv`

- **Problem**: Activation script not found
  - **Solution**: Ensure you're using the correct path: `source venv/Scripts/activate`

- **Problem**: spaCy installation errors
  - **Solution**: Try installing with: `pip install spacy==3.7.2`
  - Then download the language model: `python -m spacy download en_core_web_sm`

## Verifying Setup

1. The frontend should be accessible at: http://localhost:8080/simple-frontend.html
2. The backend should be running on: http://localhost:8000
3. You should be able to add reviews and see them displayed in the frontend
