

# user_data/strategies/scalping_strategy.py

from freqtrade.strategy import IStrategy
from user_data.modules import indicators, scoring, telegram_notifier, pattern_recognition, dynamic_pairlist, ml
import pandas as pd
import json
import os
import logging

logger = logging.getLogger(__name__)

class ScalpingStrategy(IStrategy):
    timeframe = '1m'
    startup_candle_count = 50

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.market_context = self._load_json('cache/market_context.json')
        self.sentiment_data = self._load_json('cache/sentiment_data.json')
        self.fear_greed = self._load_json('cache/fear_greed.json')
        self.pairlist = ['BTCUSDT', 'ETHUSDT']  # only scalping BTC/ETH
        self.open_positions = {}
        logger.info("ScalpingStrategy initialized.")

    def _load_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {filepath}: {e}")
            return {}

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        if metadata['pair'] not in self.pairlist:
            logger.info(f"Skipping {metadata['pair']} not in fixed pairlist for scalping.")
            return dataframe

        dataframe = indicators.add_indicators(dataframe)
        dataframe = indicators.add_advanced_indicators(dataframe)
        dataframe = pattern_recognition.add_patterns(dataframe)

        dataframe['breakout_score'] = dataframe.apply(lambda row: scoring.calculate_breakout_score(row, self.market_context), axis=1)
        dataframe['volatility_zone'] = dataframe['volatility'].apply(scoring.determine_volatility_zone)
        dataframe['ml_prediction'] = dataframe.apply(lambda row: ml.predict_price_movement(metadata['pair'], [
            row['rsi'], row['macd'], row['ema20'], row['ema50'], row['volatility'], row['breakout_score']
        ]), axis=1)

        logger.info(f"Indicators, patterns, ML prediction populated for {metadata['pair']}")
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        buy_condition = (
            (dataframe['breakout_score'] >= 4) &
            (dataframe['volatility_zone'].isin(['Very Low', 'Low'])) &
            (dataframe['ml_prediction'] >= 0) &
            (dataframe['rsi'] >= 45) & (dataframe['rsi'] <= 65) &
            (dataframe['close'] > dataframe['ema20'])
        )
        dataframe.loc[buy_condition, 'buy'] = 1

        for idx, row in dataframe[buy_condition].iterrows():
            entry_price = row['close']
            tp = entry_price * 1.002  # 0.2% target
            sl = entry_price * 0.998  # 0.2% stop
            telegram_notifier.send_trade_alert(
                metadata['pair'],
                row['breakout_score'],
                f"SCALP BUY\nEntry: {entry_price:.4f}\nTP: {tp:.4f}\nSL: {sl:.4f}",
                tp, sl
            )
            logger.info(f"SCALP BUY {metadata['pair']} entry={entry_price:.4f} TP={tp:.4f} SL={sl:.4f}")
            self.open_positions[metadata['pair']] = entry_price
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        if metadata['pair'] in self.open_positions:
            entry = self.open_positions[metadata['pair']]
            current = dataframe['close'].iloc[-1]
            percent_gain = round((current - entry) / entry * 100, 4)

            if current >= entry * 1.002 or current <= entry * 0.998:
                dataframe.loc[:, 'sell'] = 1
                telegram_notifier.send_trade_alert(
                    metadata['pair'],
                    None,
                    f"SCALP SELL\nEntry: {entry:.4f}\nExit: {current:.4f}\nResult: {percent_gain}%",
                    None, None
                )
                logger.info(f"SCALP SELL {metadata['pair']} at {current:.4f} gain {percent_gain}%")
                del self.open_positions[metadata['pair']]
        return dataframe