# user_data/modules/reddit_api.py

import requests
import logging
logger = logging.getLogger(__name__)

def fetch_reddit_mentions(symbol: str) -> int:
    try:
        url = "https://www.reddit.com/r/CryptoCurrency/hot.json?limit=50"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        mentions = sum(symbol.lower() in post['data']['title'].lower() for post in data['data']['children'])
        logger.info(f"Reddit mentions for {symbol}: {mentions}")
        return mentions
    except Exception as e:
        logger.error(f"Error fetching Reddit mentions for {symbol}: {e}")
        return 0