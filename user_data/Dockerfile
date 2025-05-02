FROM python:3.10-slim

# Install build tools and ta-lib system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    git \
    libffi-dev \
    libssl-dev \
    libta-lib0 \
    libta-lib0-dev \
    && apt-get clean

# Install ta-lib from source to satisfy talib-binary requirement
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && make && make install && \
    cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

ENV LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Set default command to start the supervisor
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]