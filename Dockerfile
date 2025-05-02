FROM python:3.10-slim

# Note: this Dockerfile is structurally correct for installing ta-lib, but Railway and similar platforms may hit resource/time limits or network restrictions during the manual source compilation step.

# Install build tools + ta-lib C library
RUN apt-get update && apt-get install -y build-essential wget gcc make \
    libffi-dev libssl-dev libxml2-dev libxslt-dev zlib1g-dev git \
    && wget https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download -O ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib && ./configure --prefix=/usr \
    && make && make install \
    && cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure /usr/lib and /usr/local/lib are used for dynamic linking
ENV LD_LIBRARY_PATH=/usr/lib:/usr/local/lib

# Now install python deps
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app
WORKDIR /app

# Start app
CMD ["python", "-m", "freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "MyStrategy"]