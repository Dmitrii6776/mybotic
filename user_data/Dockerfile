FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libta-lib0 \
    libta-lib-dev \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]