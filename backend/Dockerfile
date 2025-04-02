FROM python:3.9-slim

WORKDIR /app

# Create directory for SQLite database
RUN mkdir -p /app/data

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SpaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "run.py"]
