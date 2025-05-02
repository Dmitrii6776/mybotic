# user_data/modules/indicators.py

import logging
import pandas as pd
import talib.abstract as ta

logger = logging.getLogger(__name__)

def add_indicators(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Add basic technical indicators using TA-Lib and Freqtrade's recommended style.
    Compatible with Freqtrade indicator caching and batch operations.
    """
    logger.info("Adding basic indicators...")
    dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
    dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
    dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
    dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
    macd = ta.MACD(dataframe)
    dataframe['macd'] = macd['macd']
    dataframe['macdsignal'] = macd['macdsignal']
    dataframe['macdhist'] = macd['macdhist']
    bb = ta.BBANDS(dataframe)
    dataframe['bb_upper'] = bb['upperband']
    dataframe['bb_middle'] = bb['middleband']
    dataframe['bb_lower'] = bb['lowerband']
    dataframe['parabolic_sar'] = ta.SAR(dataframe)
    stoch = ta.STOCH(dataframe)
    dataframe['stoch_k'] = stoch['slowk']
    dataframe['stoch_d'] = stoch['slowd']
    dataframe['adx'] = ta.ADX(dataframe)
    dataframe['volatility'] = ((dataframe['high'] - dataframe['low']) / dataframe['low']) * 100
    logger.info("Basic indicators added.")
    return dataframe

def add_advanced_indicators(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Add advanced technical indicators: ATR, simplified Fibonacci, Ichimoku Cloud.
    Uses TA-Lib directly; can be replaced with pandas-ta for Freqtrade's built-in access.
    """
    logger.info("Adding advanced indicators...")
    dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
    dataframe['fibonacci_retracement'] = dataframe['close'] / dataframe['close'].rolling(100).max()  # simplification
    ichimoku = ta.ICHIMOKU(dataframe)
    dataframe['ichimoku_senkou_span_a'] = ichimoku['senkou_span_a']
    dataframe['ichimoku_senkou_span_b'] = ichimoku['senkou_span_b']
    dataframe['ichimoku_kijun_sen'] = ichimoku['kijun_sen']
    logger.info("Advanced indicators added.")
    return dataframe