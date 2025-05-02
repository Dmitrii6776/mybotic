# user_data/modules/scoring.py

import logging
logger = logging.getLogger(__name__)

def determine_volatility_zone(volatility: float) -> str:
    """Classify volatility into zones."""
    if volatility < 2:
        return 'Very Low'
    elif volatility < 4:
        return 'Low'
    elif volatility < 7:
        return 'Medium'
    elif volatility < 12:
        return 'High'
    else:
        return 'Very High'

def is_macd_bullish(row): 
    result = row['macd'] > row['macdsignal']
    logger.debug(f"MACD bullish: {result}")
    return result

def is_bollinger_breakout(row): 
    result = row['close'] > row['bb_upper']
    logger.debug(f"Bollinger breakout: {result}")
    return result

def is_ichimoku_bullish(row): 
    result = row['close'] > row.get('ichimoku_kijun_sen', row['ema20'])
    logger.debug(f"Ichimoku bullish: {result}")
    return result

def is_atr_expanding(row): 
    result = row['atr'] > row['atr'].rolling(10).mean()
    logger.debug(f"ATR expanding: {result}")
    return result

def calculate_breakout_score(row, context_data=None) -> int:
    """Calculate a composite breakout score using multiple indicators and optionally market context."""
    score = 0
    if row['rsi'] > 55: score += 1
    if row['close'] > row['ema20']: score += 1
    if row['ema20'] > row['ema50']: score += 1
    if row['ema50'] > row['ema200']: score += 1
    if is_bollinger_breakout(row): score += 1
    if is_macd_bullish(row): score += 1
    if is_ichimoku_bullish(row): score += 1
    if is_atr_expanding(row): score += 1
    if row['volatility'] >= 7: score += 1

    if context_data:
        if context_data.get('btc_dominance') and context_data['btc_dominance'] < 50: score += 1
        if context_data.get('total_market_cap') and context_data['total_market_cap'] > 500_000_000_000: score += 1

    logger.info(f"Score for {row.get('symbol', 'unknown')}: {score}")
    return score