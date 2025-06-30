# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js and npm
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend code
COPY src/ ./src/
COPY package.json package-lock.json ./
COPY next.config.ts tsconfig.json ./

# Install frontend dependencies and build Next.js app
RUN npm install
RUN npm run build

# Expose ports
EXPOSE 8000 3000

# Start backend and frontend concurrently
CMD ["sh", "-c", "uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 & npm run start"]
