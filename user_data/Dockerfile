FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y build-essential libta-lib0 libta-lib-dev

# Install pip deps
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy your app
COPY . /app/

WORKDIR /app

# Start supervisor
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]