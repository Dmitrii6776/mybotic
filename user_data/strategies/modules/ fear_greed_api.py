# user_data/modules/fear_greed_api.py

import requests
import logging
logger = logging.getLogger(__name__)

def fetch_fear_greed_index() -> dict:
    try:
        url = "https://api.alternative.me/fng/"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()['data'][0]
        result = {"score": int(data['value']), "classification": data['value_classification']}
        logger.info(f"Fear & Greed index: {result}")
        return result
    except Exception as e:
        logger.error(f"Error fetching Fear & Greed index: {e}")
        return {"score": None, "classification": "unknown"}