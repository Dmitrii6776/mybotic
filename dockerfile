FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt supervisor

COPY supervisord.conf /app/supervisord.conf

EXPOSE 8000

CMD ["supervisord", "-c", "/app/supervisord.conf"]