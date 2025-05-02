# Use a base image with python
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    make \
    wget \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Download and build TA-Lib (C library)
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O /tmp/ta-lib.tar.gz \
    && tar -xzf /tmp/ta-lib.tar.gz -C /tmp \
    && cd /tmp/ta-lib && ./configure --prefix=/usr && make && make install \
    && rm -rf /tmp/ta-lib*

# Tell linker where to find TA-Lib
ENV LD_LIBRARY_PATH="/usr/lib"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app
WORKDIR /app

# Set environment (optional if your app needs)
ENV FREQTRADE_HOME=/app/user_data

# Command to start Freqtrade or server
CMD ["freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "hype_strategy"]