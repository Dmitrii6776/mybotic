# user_data/modules/pattern_recognition.py

import talib.abstract as ta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def detect_head_shoulders(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLHEADANDSHOULDERS(dataframe)
    logger.debug(f"Head and Shoulders pattern detected: {pattern[pattern != 0].count()}")
    return pattern

def detect_triangles(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLTRISTAR(dataframe)
    logger.debug(f"Triangle pattern detected: {pattern[pattern != 0].count()}")
    return pattern

def detect_flags(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLHIGHWAVE(dataframe)  # High wave as proxy for flags
    logger.debug(f"Flag pattern detected: {pattern[pattern != 0].count()}")
    return pattern

def detect_morning_star(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLMORNINGSTAR(dataframe)
    logger.debug(f"Morning Star detected: {pattern[pattern != 0].count()}")
    return pattern

def detect_evening_star(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLEVENINGSTAR(dataframe)
    logger.debug(f"Evening Star detected: {pattern[pattern != 0].count()}")
    return pattern

def detect_bullish_engulfing(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLENGULFING(dataframe)
    logger.debug(f"Bullish Engulfing detected: {pattern[pattern > 0].count()}")
    return pattern

def detect_bearish_engulfing(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLENGULFING(dataframe)
    logger.debug(f"Bearish Engulfing detected: {pattern[pattern < 0].count()}")
    return pattern

def detect_hammer(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLHAMMER(dataframe)
    logger.debug(f"Hammer detected: {pattern[pattern != 0].count()}")
    return pattern

def detect_shooting_star(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLSHOOTINGSTAR(dataframe)
    logger.debug(f"Shooting Star detected: {pattern[pattern != 0].count()}")
    return pattern

def add_patterns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['head_shoulders'] = detect_head_shoulders(dataframe)
    dataframe['triangle'] = detect_triangles(dataframe)
    dataframe['flag'] = detect_flags(dataframe)
    dataframe['morning_star'] = detect_morning_star(dataframe)
    dataframe['evening_star'] = detect_evening_star(dataframe)
    dataframe['bullish_engulfing'] = detect_bullish_engulfing(dataframe)
    dataframe['bearish_engulfing'] = detect_bearish_engulfing(dataframe)
    dataframe['hammer'] = detect_hammer(dataframe)
    dataframe['shooting_star'] = detect_shooting_star(dataframe)
    logger.info("Pattern recognition indicators added to dataframe.")
    return dataframe