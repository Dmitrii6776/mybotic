# user_data/modules/cryptopanic_api.py

import requests
import logging
import json
import os

logger = logging.getLogger(__name__)

# Load config.json once
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

API_KEY = config.get('API_Keys', {}).get('crypto_panic')

def fetch_news_sentiment(symbol: str) -> str:
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&currencies={symbol}&public=true"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        votes = [p['votes']['positive'] - p['votes']['negative'] for p in data.get('results', [])]
        avg_vote = sum(votes) / len(votes) if votes else 0
        sentiment = "positive" if avg_vote > 0 else "neutral" if avg_vote == 0 else "negative"
        logger.info(f"News sentiment for {symbol}: {sentiment}")
        return sentiment
    except Exception as e:
        logger.error(f"Error fetching news sentiment for {symbol}: {e}")
        return "neutral"