FROM python:3.11-slim

# Install system dependencies (including ta-lib C library and headers)
RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0 \
    libta-lib-dev \
    supervisor \
    && apt-get clean

# Set workdir
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the app
COPY . .

# Expose app port (uvicorn)
EXPOSE 8000

# Start supervisord (runs both freqtrade and API server)
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]