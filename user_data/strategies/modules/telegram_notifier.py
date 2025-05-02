# user_data/modules/telegram_notifier.py

import requests
import logging
import json
import os

logger = logging.getLogger(__name__)

# Load config.json once
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

TELEGRAM_TOKEN = config.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = config.get('TELEGRAM_CHAT_ID')

def send_trade_alert(symbol, score, signal, tp, sl):
    message = f\"🚀 {signal} Signal for {symbol}\\nBreakout Score: {score}\\nTP: {tp}\\nSL: {sl}\"
    url = f\"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage\"
    params = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        response = requests.get(url, params=params)
        logger.info(f\"Sent Telegram alert for {symbol}: {response.status_code}\")
    except Exception as e:
        logger.error(f\"Telegram alert failed for {symbol}: {e}\")