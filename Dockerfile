FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc build-essential libportaudio2 portaudio19-dev && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU-only versions explicitly to avoid CUDA dependencies
RUN pip install torch==2.0.1 torchvision==0.15.2 -f https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]