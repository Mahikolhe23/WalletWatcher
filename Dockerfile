# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy code (not needed for dev because of volume mount, but good for fallback)
COPY . .

# Default command (can be overridden)
CMD ["python", "main.py"]
