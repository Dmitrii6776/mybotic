# user_data/modules/bybit_api.py

import requests
from requests.adapters import HTTPAdapter
import json
import logging
import os

logger = logging.getLogger(__name__)

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=3))

def fetch_market_data(write_cache=False):
    url = 'https://api.bybit.com/v5/market/tickers?category=spot'
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        tickers = {item['symbol']: item for item in data.get('result', {}).get('list', [])}
        logger.info(f"Fetched {len(tickers)} tickers from Bybit.")
        if write_cache:
            os.makedirs('cache', exist_ok=True)
            with open('cache/market_data.json', 'w') as f:
                json.dump(tickers, f)
        return tickers
    except Exception as e:
        logger.error(f"Failed to fetch market data: {e}")
        return {}

def fetch_orderbook(symbol, write_cache=False):
    url = f'https://api.bybit.com/v5/market/orderbook?category=spot&symbol={symbol}&limit=5'
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get('result', {})
        logger.info(f"Fetched orderbook for {symbol}")
        if write_cache:
            os.makedirs('cache', exist_ok=True)
            with open(f'cache/orderbook_{symbol}.json', 'w') as f:
                json.dump(data, f)
        return data
    except Exception as e:
        logger.error(f"Failed to fetch orderbook for {symbol}: {e}")
        return {}

def fetch_candles(symbol, interval='60', write_cache=False):
    url = f'https://api.bybit.com/v5/market/kline?category=spot&symbol={symbol}&interval={interval}'
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get('result', {}).get('list', [])
        logger.info(f"Fetched {len(data)} candles for {symbol}")
        if write_cache:
            os.makedirs('cache', exist_ok=True)
            with open(f'cache/candles_{symbol}_{interval}.json', 'w') as f:
                json.dump(data, f)
        return data
    except Exception as e:
        logger.error(f"Failed to fetch candles for {symbol}: {e}")
        return {}