FROM jakobkallestad/ta-lib:python3.10-slim

# Ensure correct dynamic library paths (just in case)
ENV LD_LIBRARY_PATH=/usr/lib:/usr/local/lib

WORKDIR /app

# Install Python dependencies (no need to build ta-lib → already installed in base image!)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Start app
CMD ["python", "-m", "freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "MyStrategy"]