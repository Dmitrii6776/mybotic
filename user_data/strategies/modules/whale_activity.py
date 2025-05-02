

# user_data/modules/whale_activity.py

import asyncio
import json
import os
import logging
from telethon import TelegramClient

logger = logging.getLogger(__name__)

API_ID = 28567007
API_HASH = '900ec02c4614f2bb7a2f40b5d326421e'
SESSION_NAME = 'whale_session'
CHANNEL = '@CryptoWhaleBot'
CACHE_PATH = 'cache/whale_activity.json'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def fetch_whale_messages(limit=50):
    try:
        await client.start()
        messages = []
        async for message in client.iter_messages(CHANNEL, limit=limit):
            if message.text:
                messages.append(message.text)
        logger.info(f"Fetched {len(messages)} messages from {CHANNEL}" )
        return messages
    except Exception as e:
        logger.error(f"Error fetching whale messages: {e}")
        return []

def parse_messages(messages):
    parsed = []
    for msg in messages:
        try:
            if 'Transaction' in msg or 'transfer' in msg:
                entry = {'raw': msg}
                if '$' in msg:
                    usd_amount = msg.split('$')[1].split()[0].replace(',', '')
                    entry['usd_amount'] = float(usd_amount)
                if 'BTC' in msg: entry['symbol'] = 'BTC'
                if 'ETH' in msg: entry['symbol'] = 'ETH'
                if 'USDT' in msg: entry['symbol'] = 'USDT'
                if 'Binance' in msg: entry['exchange'] = 'Binance'
                if 'Kraken' in msg: entry['exchange'] = 'Kraken'
                parsed.append(entry)
        except Exception as e:
            logger.warning(f"Failed to parse message: {msg[:30]}... {e}")
    logger.info(f"Parsed {len(parsed)} whale activity records.")
    return parsed

def save_whale_activity(data):
    os.makedirs('cache', exist_ok=True)
    with open(CACHE_PATH, 'w') as f:
        json.dump(data, f)
    logger.info(f"Whale activity saved to {CACHE_PATH}")

def update_whale_activity():
    loop = asyncio.get_event_loop()
    messages = loop.run_until_complete(fetch_whale_messages())
    parsed = parse_messages(messages)
    save_whale_activity(parsed)