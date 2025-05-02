FROM python:3.10-slim

# Install TA-Lib system library & compiler tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0 \
    libta-lib-dev \
    && apt-get clean

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install pip packages AFTER system library is available
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your project code
COPY . .

# Expose port (optional for API)
EXPOSE 8000

# Run supervisor to launch both freqtrade + API server
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]