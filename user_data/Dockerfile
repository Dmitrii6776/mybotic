FROM python:3.10-slim

# Install build tools and ta-lib system libs
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    libta-lib0 \
    libta-lib0-dev \
    && apt-get clean

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Default command
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]