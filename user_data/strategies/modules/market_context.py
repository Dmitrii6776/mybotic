# user_data/modules/market_context.py

import requests
import json
import logging
import os

logger = logging.getLogger(__name__)

# Load config.json
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

def fetch_btc_dominance():
    try:
        url = 'https://api.coingecko.com/api/v3/global'
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        dominance = data['data']['market_cap_percentage']['btc']
        logger.info(f"BTC dominance: {dominance:.2f}%")
        return dominance
    except Exception as e:
        logger.error(f"Error fetching BTC dominance: {e}")
        return None

def fetch_total_market_cap():
    try:
        url = 'https://api.coingecko.com/api/v3/global'
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        market_cap = data['data']['total_market_cap']['usd']
        logger.info(f"Total market cap: {market_cap / 1e9:.2f}B USD")
        return market_cap
    except Exception as e:
        logger.error(f"Error fetching total market cap: {e}")
        return None

def fetch_eth_btc_ratio():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin&vs_currencies=btc'
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        ratio = data['ethereum']['btc']
        logger.info(f"ETH/BTC ratio: {ratio:.4f}")
        return ratio
    except Exception as e:
        logger.error(f"Error fetching ETH/BTC ratio: {e}")
        return None

def fetch_market_context(write_cache=True):
    context = {
        'btc_dominance': fetch_btc_dominance(),
        'total_market_cap': fetch_total_market_cap(),
        'eth_btc_ratio': fetch_eth_btc_ratio()
    }
    if write_cache:
        os.makedirs('cache', exist_ok=True)
        with open('cache/market_context.json', 'w') as f:
            json.dump(context, f)
        logger.info("Market context saved to cache/market_context.json")
    return context
