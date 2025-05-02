# user_data/modules/dynamic_pairlist.py

import json
import os
import logging

logger = logging.getLogger(__name__)

def load_market_data(cache_path='cache/market_data.json'):
    """Load cached market data (from Bybit API fetch)."""
    try:
        with open(cache_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} market symbols from cache.")
        return data
    except Exception as e:
        logger.error(f"Error loading market data: {e}")
        return {}

def generate_pairlist(min_volume_usdt=1_000_000, max_spread_percent=0.5):
    """
    Generate a dynamic pairlist filtered by volume and spread thresholds.
    Returns a list of symbol strings (e.g., BTCUSDT).
    """
    market_data = load_market_data()
    pairs = []
    for symbol, info in market_data.items():
        try:
            volume = float(info.get('turnover24h', 0))
            spread = abs(float(info.get('ask1Price', 0)) - float(info.get('bid1Price', 0))) / float(info.get('ask1Price', 1)) * 100 if float(info.get('ask1Price', 0)) > 0 else 100
            if volume >= min_volume_usdt and spread <= max_spread_percent:
                pairs.append(symbol)
        except Exception as e:
            logger.warning(f"Skipping symbol {symbol}: {e}")
    logger.info(f"Dynamic pairlist generated: {len(pairs)} pairs meet criteria.")
    return pairs

def save_pairlist(pairs, output_path='cache/pairlist.json'):
    try:
        os.makedirs('cache', exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(pairs, f)
        logger.info(f"Pairlist saved to {output_path} ({len(pairs)} pairs).")
    except Exception as e:
        logger.error(f"Error saving pairlist: {e}")
