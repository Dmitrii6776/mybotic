# Use Alpine (lightweight) or switch to python:3.11-slim if you want debian-based
FROM python:3.11-alpine

# Install required build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libc-dev \
    g++ \
    make \
    bash \
    tar \
    libffi-dev \
    openssl-dev \
    libxml2-dev \
    libxslt-dev \
    zlib-dev \
    linux-headers \
    build-base \
    wget

# Copy the ta-lib source tar.gz into container
COPY resources/ta-lib-0.4.0-src.tar.gz /tmp/ta-lib-0.4.0-src.tar.gz

# Build and install ta-lib
RUN cd /tmp && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib-0.4.0 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    rm -rf /tmp/ta-lib-0.4.0*

# Set environment paths
ENV TA_LIBRARY_PATH=/usr/lib
ENV TA_INCLUDE_PATH=/usr/include

# Create virtualenv
ENV VENV_PATH=.venv
RUN python3.11 -m pip install virtualenv && \
    python3.11 -m virtualenv -p python3.11 $VENV_PATH

ENV PATH=$VENV_PATH/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Pin compatible numpy version first
RUN pip install numpy==2.2.0

# Install ta-lib python wrapper
RUN pip install TA-Lib==0.6.1

# Install rest of your requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . /app
WORKDIR /app

# Start the app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]