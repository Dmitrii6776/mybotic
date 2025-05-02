FROM python:3.11-slim

# Install required system libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0 \
    libta-lib-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose ports
EXPOSE 8000

# Start both freqtrade and API via supervisord
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]