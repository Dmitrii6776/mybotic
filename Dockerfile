FROM python:3.10-slim

# Install dependencies for building ta-lib C lib and python binding
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

# Download and build ta-lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O /tmp/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf /tmp/ta-lib-0.4.0-src.tar.gz -C /tmp && \
    cd /tmp/ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    rm -rf /tmp/*

# Create virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and install setuptools manually
RUN pip install --upgrade pip setuptools

# Clone ta-lib-python repo and build python binding
RUN pip install --upgrade pip && \
    pip install numpy==1.26.4 && \
    pip install TA-Lib -v --no-build-isolation && \
    pip install -r requirements.txt

# Copy requirements without ta-lib
COPY requirements.txt .


# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of code
COPY . .

# Start the app
CMD ["python", "your_main_script.py"]