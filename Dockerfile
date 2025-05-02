FROM python:3.10-slim

# Install build tools + ta-lib C library
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gcc \
    make \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    git \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib && ./configure --prefix=/usr && make && make install \
    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Ensure /usr/lib is used for dynamic linking
ENV LD_LIBRARY_PATH=/usr/lib

# Now install python deps
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app
WORKDIR /app

# Start app
CMD ["python", "-m", "freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "MyStrategy"]