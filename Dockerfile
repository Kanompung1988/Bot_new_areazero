# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs output

# Expose port
EXPOSE 8000

# Health check - more lenient for Discord bot startup
HEALTHCHECK --interval=45s --timeout=15s --start-period=90s --retries=5 \
    CMD python -c "import requests; r = requests.get('http://localhost:8000/health', timeout=10); exit(0 if r.status_code == 200 else 1)"

# Run the application
CMD ["python", "-u", "run_api.py"]
