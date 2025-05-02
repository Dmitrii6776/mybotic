FROM python:3.11-slim

# Install system dependencies for ta-lib
RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0 \
    libta-lib-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy your app
COPY . /app
WORKDIR /app

# Run supervisord to start freqtrade and API together
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]