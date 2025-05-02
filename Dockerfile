FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential gcc make wget libffi-dev \
    libssl-dev libxml2-dev libxslt-dev zlib1g-dev git

# Download TA-Lib 0.6.1 from official GitHub release
RUN wget https://github.com/TA-Lib/ta-lib/releases/download/v0.6.1/ta-lib-0.6.1-src.tar.gz -O /tmp/ta-lib-0.6.1-src.tar.gz && \
    cd /tmp && \
    tar -xzf ta-lib-0.6.1-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Start the app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]