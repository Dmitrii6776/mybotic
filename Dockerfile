FROM python:3.10-slim

# Install dependencies required to compile ta-lib
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    wget \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Download and build ta-lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O /tmp/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf /tmp/ta-lib-0.4.0-src.tar.gz -C /tmp && \
    cd /tmp/ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    rm -rf /tmp/*

# Environment variables for ta-lib
ENV TA_LIBRARY_PATH=/usr/lib
ENV TA_INCLUDE_PATH=/usr/include

# Create virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Start app
CMD ["python", "-m", "freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "MyStrategy"]