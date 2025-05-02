
# user_data/modules/pattern_recognition.py

import talib.abstract as ta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def detect_head_shoulders(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLHEADANDSHOULDERS(dataframe)
    logger.debug(f"Head and Shoulders pattern detected count: {pattern[pattern != 0].count()}")
    return pattern

def detect_triangles(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLTRISTAR(dataframe)
    logger.debug(f"Triangle pattern detected count: {pattern[pattern != 0].count()}")
    return pattern

def detect_flags(dataframe: pd.DataFrame) -> pd.Series:
    pattern = ta.CDLHIGHWAVE(dataframe)  # High wave as proxy for flags
    logger.debug(f"Flag pattern detected count: {pattern[pattern != 0].count()}")
    return pattern

def add_patterns(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['head_shoulders'] = detect_head_shoulders(dataframe)
    dataframe['triangle'] = detect_triangles(dataframe)
    dataframe['flag'] = detect_flags(dataframe)
    logger.info("Pattern recognition indicators added to dataframe.")
    return dataframe