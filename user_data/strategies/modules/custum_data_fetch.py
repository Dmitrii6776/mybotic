# user_data/modules/custum_data_fetch.py

import logging
import os
import json
from user_data.modules.market_context import fetch_market_context
from user_data.modules.bybit_api import fetch_market_data
from user_data.modules.reddit_api import fetch_reddit_mentions
from user_data.modules.cryptopanic_api import fetch_news_sentiment
from user_data.modules.fear_greed_api import fetch_fear_greed_index

logger = logging.getLogger(__name__)

def custom_data_fetcher(freqtrade):
    """
    Called by Freqtrade every custom_data_refresh_interval (configured in strategy).
    Refreshes cached market data, sentiment data, and context files.
    """
    logger.info("[custom_data_fetcher] Starting data refresh...")

    # Refresh market context
    context = fetch_market_context(write_cache=True)
    logger.info(f"Market context refreshed: {context}")

    # Refresh market data
    market_data = fetch_market_data(write_cache=True)
    logger.info(f"Market data refreshed: {len(market_data)} symbols.")

    # Refresh sentiment per top symbols
    symbols = list(market_data.keys())[:5]  # Example: fetch sentiment for top 5 only
    sentiment_results = {}
    for symbol in symbols:
        reddit_mentions = fetch_reddit_mentions(symbol.replace('USDT',''))
        news_sentiment = fetch_news_sentiment(symbol.replace('USDT',''))
        sentiment_results[symbol] = {
            'reddit_mentions': reddit_mentions,
            'news_sentiment': news_sentiment
        }
        logger.info(f"[{symbol}] Reddit: {reddit_mentions}, News: {news_sentiment}")

    os.makedirs('cache', exist_ok=True)
    with open('cache/sentiment_data.json', 'w') as f:
        json.dump(sentiment_results, f)

    # Refresh Fear & Greed Index
    fear_greed = fetch_fear_greed_index()
    with open('cache/fear_greed.json', 'w') as f:
        json.dump(fear_greed, f)
    logger.info(f"Fear & Greed Index refreshed: {fear_greed}")

    logger.info("[custom_data_fetcher] Data refresh complete.")
