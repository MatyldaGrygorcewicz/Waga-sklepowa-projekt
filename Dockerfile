# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Install system dependencies required for TensorFlow and Pillow
# Then clean up to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy application files
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY fruit_classifier_model.h5 /app/fruit_classifier_model.h5
COPY model_info.json /app/model_info.json

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

# Run gunicorn server
# - bind to 0.0.0.0:8080 (Cloud Run requirement)
# - 2 workers for better performance on Cloud Run
# - timeout of 300 seconds for ML model loading
# - access log to stdout for Cloud Run logging
CMD exec gunicorn --bind 0.0.0.0:8080 \
    --workers 2 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --chdir /app/backend \
    app:app
