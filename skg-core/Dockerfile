FROM python:3.11-slim

WORKDIR /app

# Install CPU-only torch first to avoid CUDA dependencies
RUN pip install --no-cache-dir torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu

COPY setup.py .
COPY skg/ ./skg/

RUN pip install --no-cache-dir -e .

EXPOSE 8004

CMD ["skg"]