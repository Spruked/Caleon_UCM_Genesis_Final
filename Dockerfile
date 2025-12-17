FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio processing and build tools
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt requirements.prod.txt ./
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs _archive cochlear_processor_v2.0 Phonatory_Output_Module

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=info

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

EXPOSE 8000

# Use uvicorn for production
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]