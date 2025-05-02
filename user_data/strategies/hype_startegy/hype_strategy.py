# user_data/strategies/hype_strategy.py

from freqtrade.strategy import IStrategy
from user_data.modules import indicators, scoring, telegram_notifier, pattern_recognition, dynamic_pairlist, ml
import pandas as pd
import json
import os
import logging

logger = logging.getLogger(__name__)

class HypeStrategy(IStrategy):
    timeframe = '1h'
    startup_candle_count = 50

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.market_context = self._load_json('cache/market_context.json')
        self.sentiment_data = self._load_json('cache/sentiment_data.json')
        self.whale_activity = self._load_json('cache/whale_activity.json')
        self.fear_greed = self._load_json('cache/fear_greed.json')
        self.pairlist = self._load_json('cache/pairlist.json')
        self.open_positions = {}  # {pair: entry_price}
        logger.info("HypeStrategy initialized with cached data.")

    def _load_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {filepath}: {e}")
            return {}

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        if metadata['pair'] not in self.pairlist:
            logger.info(f"Skipping {metadata['pair']} not in dynamic pairlist.")
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
            (dataframe['breakout_score'] >= 6) &
            (dataframe['rsi'] < 70) &
            (dataframe['close'] > dataframe['ema20']) &
            (dataframe['volatility_zone'].isin(['Low', 'Medium'])) &
            (dataframe['ml_prediction'] >= 0)
        )
        dataframe.loc[buy_condition, 'buy'] = 1

        for idx, row in dataframe[buy_condition].iterrows():
            entry_price = row['close']
            tp = entry_price * 1.02
            sl = entry_price * 0.98
            percent_target = round((tp - entry_price) / entry_price * 100, 2)
            telegram_notifier.send_trade_alert(
                metadata['pair'],
                row['breakout_score'],
                f"BUY\nEntry: {entry_price:.4f}\nTP: {tp:.4f}\nSL: {sl:.4f}\nTarget: {percent_target}%",
                tp, sl
            )
            logger.info(f"BUY Signal {metadata['pair']} score={row['breakout_score']} TP={tp} SL={sl}")
            self.open_positions[metadata['pair']] = entry_price  # remember entry price
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        if metadata['pair'] in self.open_positions:
            entry = self.open_positions[metadata['pair']]
            current = dataframe['close'].iloc[-1]
            percent_gain = round((current - entry) / entry * 100, 2)

            if current >= entry * 1.02 or current <= entry * 0.98:
                dataframe.loc[:, 'sell'] = 1
                telegram_notifier.send_trade_alert(
                    metadata['pair'],
                    None,
                    f"SELL\nEntry: {entry:.4f}\nExit: {current:.4f}\nResult: {percent_gain}%",
                    None, None
                )
                logger.info(f"SELL Signal {metadata['pair']} at {current:.4f} gain {percent_gain}%")
                del self.open_positions[metadata['pair']]  # remove tracked position
        return dataframe

    def custom_data_fetcher(self, pair, dataframe: pd.DataFrame, metadata: dict) -> None:
        """Runs every X candles to refresh cached data."""
        from user_data.modules.custum_data_fetch import custom_data_fetcher
        custom_data_fetcher(self)
        self.market_context = self._load_json('cache/market_context.json')
        self.sentiment_data = self._load_json('cache/sentiment_data.json')
        self.whale_activity = self._load_json('cache/whale_activity.json')
        self.fear_greed = self._load_json('cache/fear_greed.json')
        self.pairlist = self._load_json('cache/pairlist.json')
        logger.info("[custom_data_fetcher] Refreshed cached data reloaded.")