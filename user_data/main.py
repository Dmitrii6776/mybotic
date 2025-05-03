import json
import logging
import os

from user_data.strategies.hype_startegy.hype_strategy import HypeStrategy
from user_data.strategies.scalping_strategy.scalping_strategy import ScalpingStrategy

from strategies.modules import (
    bybit_api,
    cryptopanic_api,
    custum_data_fetch,
    dynamic_pairlist,
    fear_greed_api,
    indicators,
    market_context,
    ml,
    pattern_recognition,
    reddit_api,
    scoring,
    telegram_notifier,
    whale_activity,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load config
config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.exists(config_path):
    logger.error(f"Config file not found at {config_path}")
    config = {}
else:
    with open(config_path, "r") as f:
        config = json.load(f)

# Fetch data from modules
def fetch_data():
    logger.info("Fetching data from modules...")
    market_data = bybit_api.get_market_data()
    sentiment_data = fear_greed_api.get_fear_and_greed_index()
    news_data = cryptopanic_api.get_latest_news()
    reddit_data = reddit_api.get_trending_coins()
    whale_data = whale_activity.get_whale_alerts()
    pairlist = dynamic_pairlist.get_pairs()
    custom_data = custum_data_fetch.get_custom_data()

    metadata = {
        "market_data": market_data,
        "sentiment_data": sentiment_data,
        "news_data": news_data,
        "reddit_data": reddit_data,
        "whale_data": whale_data,
        "pairlist": pairlist,
        "custom_data": custom_data,
    }

    logger.info("Data fetched successfully.")
    return metadata

def run_strategies():
    metadata = fetch_data()

    # Create DataFrame from market data or other module outputs
    df = indicators.prepare_dataframe(metadata["market_data"])

    logger.info("Running HypeStrategy...")
    hype_strategy = HypeStrategy()
    hype_signals = hype_strategy.populate_indicators(df, metadata)

    logger.info("Running ScalpingStrategy...")
    scalp_strategy = ScalpingStrategy()
    scalp_signals = scalp_strategy.populate_indicators(df, metadata)

    logger.info("Processing signals...")
    for signal in hype_signals:
        telegram_notifier.send_trade_alert(**signal)

    for signal in scalp_signals:
        telegram_notifier.send_trade_alert(**signal)

if __name__ == "__main__":
    logger.info("Starting main strategy runner...")
    run_strategies()
