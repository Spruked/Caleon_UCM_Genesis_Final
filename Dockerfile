FROM python:3.11-slim

WORKDIR /app

# Install build dependencies (CPU-only, no GPU/CUDA)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libportaudio2 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (CPU-only versions)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set Python path to include the app directory
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "main.py"]