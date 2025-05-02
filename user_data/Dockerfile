FROM python:3.10-slim

# Install build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    gcc \
    g++ \
    make \
    && apt-get clean

# Download and build TA-Lib C library from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O /tmp/ta-lib.tar.gz \
    && tar -xvzf /tmp/ta-lib.tar.gz -C /tmp \
    && cd /tmp/ta-lib && ./configure --prefix=/usr && make && make install \
    && rm -rf /tmp/ta-lib /tmp/ta-lib.tar.gz

# Set environment variables for TA-Lib
ENV TA_LIBRARY_PATH=/usr/lib
ENV TA_INCLUDE_PATH=/usr/include

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

EXPOSE 8000

# Run supervisord
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]