# Review Analysis App - Troubleshooting Guide

This guide addresses common issues you might encounter when setting up and running the Review Analysis App on Windows using Git Bash.

## Frontend Issues

### Issue: Opening simple-frontend.html directly shows raw HTML code

**Cause**: 
When opening HTML files directly from the file system (using the `file://` protocol), modern browsers enforce security restrictions that prevent JavaScript from making API requests to different domains or protocols. This is known as the Same-Origin Policy.

**Solution**:
1. Use a local web server to serve the HTML file:
   ```bash
   cd /path/to/ReviewAnalysisApp
   python -m http.server 8080
   ```

2. Access the frontend through the web server:
   ```
   http://localhost:8080/simple-frontend.html
   ```

### Issue: Frontend can't connect to the backend

**Cause**:
The frontend is configured to connect to a specific port, but the backend might be running on a different port.

**Solution**:
1. Check that the backend is running (you should see terminal output)
2. Verify the API_URL in simple-frontend.html matches the port your backend is running on:
   ```javascript
   const API_URL = 'http://localhost:8000/api';
   ```
3. Open your browser's developer tools (F12) and check the Console tab for any error messages
4. If you see CORS errors, ensure the backend has proper CORS configuration

## Backend Issues

### Issue: Virtual environment creates in C:\Program Files\Git\venv

**Cause**:
Git Bash on Windows interprets paths differently than Windows Command Prompt. When you run `python -m venv venv`, Git Bash creates the virtual environment in its own installation directory.

**Solution**:
1. Use an absolute Windows path with the correct format:
   ```bash
   python -m venv /c/Users/YourUsername/path/to/ReviewAnalysisApp/venv
   ```
   
2. Alternatively, use Windows Command Prompt instead of Git Bash for this step:
   ```cmd
   python -m venv venv
   ```

### Issue: venv\Scripts\activate doesn't work

**Cause**:
The activation script path might be incorrect, or you might be using the wrong syntax for Git Bash.

**Solution**:
1. In Git Bash, use the source command with forward slashes:
   ```bash
   source venv/Scripts/activate
   ```

2. If that doesn't work, try the full path:
   ```bash
   source /c/Users/YourUsername/path/to/ReviewAnalysisApp/venv/Scripts/activate
   ```

### Issue: requirements.txt not found

**Cause**:
You might not be in the correct directory, or the file might not exist.

**Solution**:
1. Verify you're in the correct directory:
   ```bash
   pwd
   ls -la
   ```

2. For the simple backend, you can install dependencies directly:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

### Issue: spaCy installation errors

**Cause**:
spaCy can be complex to install due to its dependencies.

**Solution**:
1. Install spaCy with a specific version:
   ```bash
   pip install spacy==3.7.2
   ```

2. Download the language model separately:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. If you're still having issues, try installing without the language model first:
   ```bash
   pip install spacy==3.7.2
   ```
   Then download the model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Port Usage Confusion

### Issue: Confusion about which ports to use

**Clarification**:
- **Backend**: Runs on port 8000 (Python/FastAPI)
- **Frontend**: Served on port 8080 (Python's http.server)

The frontend makes API requests to the backend at http://localhost:8000/api.

**Solution**:
1. Make sure the backend is running on port 8000:
   ```bash
   python simple-backend.py
   # or
   python run.py
   ```

2. Make sure the frontend is configured to connect to port 8000:
   ```javascript
   const API_URL = 'http://localhost:8000/api';
   ```

3. Access the frontend through port 8080:
   ```
   http://localhost:8080/simple-frontend.html
   ```

## Permission Issues

### Issue: Permission errors when running scripts

**Cause**:
Windows security settings might prevent scripts from running.

**Solution**:
1. Run Git Bash as Administrator
2. Check file permissions:
   ```bash
   ls -la
   ```
3. Make scripts executable if needed:
   ```bash
   chmod +x simple-backend.py
   ```
