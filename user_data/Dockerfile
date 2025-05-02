FROM python:3.11-slim

# Install required OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0 \
    libta-lib-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port (if needed by FastAPI/uvicorn)
EXPOSE 8000

# Run via supervisord (since your project uses it)
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]