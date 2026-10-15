FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python packages
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy source code, datasets, and scripts
COPY backend /app/backend
COPY data /app/data
COPY models /app/models

WORKDIR /app/backend

# Expose FastAPI port
EXPOSE 8000

# Train model if not present and start server
CMD ["sh", "-c", "python -m app.ml.train && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
