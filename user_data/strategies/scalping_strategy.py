import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd
import pandas_ta as pta
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import requests
import json


class scalp_strategy(IStrategy):
    """
    This strategy is designed for scalping, aiming for small profits within a 1-hour timeframe.
    """
    INTERFACE_VERSION = 3

    # --- Strategy Configuration ---
    timeframe = '5m'
    minimal_roi = {"0": 0.03, "10": 0.01, "20": 0.005, "30": 0}
    stoploss = -0.03
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    startup_candle_count: int = 20
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # --- Indicator Definitions ---
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several indicators to the given DataFrame.

        Args:
            dataframe (DataFrame): The input DataFrame.
            metadata (dict): Additional metadata.

        Returns:
            DataFrame: The DataFrame with added indicators.
        """
        # -- Momentum Indicators --
        dataframe['rsi'] = pta.rsi(dataframe['close'], length=7)

        # -- Trend Indicators --
        dataframe['ema_fast'] = pta.ema(dataframe['close'], length=9)
        dataframe['ema_slow'] = pta.ema(dataframe['close'], length=21)

        # -- Volatility Indicator --
        dataframe['atr'] = pta.atr(dataframe['high'], dataframe['low'], dataframe['close'], length=7)
        dataframe['atr_pcnt'] = (dataframe['atr'] / dataframe['close']) * 100

        # -- Volume --
        dataframe['volume_sma'] = pta.sma(dataframe['volume'], length=10)

        # --- Custom Logic / Combined Signals ---
        # 1. Determine Volatility Zone
        dataframe.loc[dataframe['atr_pcnt'] <= 0.3, 'volatility_zone'] = 'Very Low'
        dataframe.loc[(dataframe['atr_pcnt'] > 0.3) & (dataframe['atr_pcnt'] <= 0.6), 'volatility_zone'] = 'Low'
        dataframe.loc[(dataframe['atr_pcnt'] > 0.6) & (dataframe['atr_pcnt'] <= 1.0), 'volatility_zone'] = 'Medium'
        dataframe.loc[dataframe['atr_pcnt'] > 1.0, 'volatility_zone'] = 'High'

        # 2. Momentum Health
        dataframe.loc[dataframe['rsi'] > 70, 'momentum_health'] = 'Overbought'
        dataframe.loc[(dataframe['rsi'] >= 40) & (dataframe['rsi'] <= 60), 'momentum_health'] = 'Healthy'
        dataframe.loc[dataframe['rsi'] < 30, 'momentum_health'] = 'Oversold'
        dataframe['momentum_health'] = dataframe['momentum_health'].fillna('Neutral')

        # 3. Basic Trend Confirmation
        dataframe['trend_confirmed'] = (dataframe['close'] > dataframe['ema_slow']).astype('int')

        # 4. Volume Check
        dataframe['volume_spike'] = (dataframe['volume'] > dataframe['volume_sma'] * 1.5).astype('int')

        return dataframe

    def send_telegram_message(self, message: str):
        """
        Sends a message to the specified Telegram chat.

        Args:
            message (str): The message to send.
        """
        bot_token = '7909214002:AAFD9sOWssN1_EQr8b16pJ7va-HDZqcVC0k'
        chat_id = '433684845'
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            
    def populate_ai_signals(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the buy and sell signals based on the AI model.
        
        Args:
            dataframe (DataFrame): The input DataFrame.
            metadata (dict): Additional metadata.

        Returns:
            DataFrame: The DataFrame with added AI signals
        """
        # The AI model will populate 'enter_tag' and 'exit_tag' based on its predictions.
        return dataframe

    # --- Buy Signal Logic ---
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe.
        """
        # --- Combine conditions to approximate the 'Breakout Score' concept ---
        buy_conditions = []
        buy_conditions.append(dataframe['trend_confirmed'] == 1)
        buy_conditions.append(dataframe['momentum_health'] == 'Healthy')
        buy_conditions.append(dataframe['volatility_zone'].isin(['Very Low', 'Low', 'Medium']))
        buy_conditions.append(dataframe['volume_spike'] == 1)
        buy_conditions.append(qtpylib.crossed_above(dataframe['ema_fast'], dataframe['ema_slow']))

        if buy_conditions:
            dataframe.loc[
                (pd.concat(buy_conditions, axis=1)).all(axis=1),
                'enter_long'] = 1
            self.send_telegram_message(f"Buy signal detected for {metadata['pair']}!")

        return dataframe

    # --- Sell Signal Logic ---
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe.
        """
        sell_conditions = []
        sell_conditions.append(dataframe['rsi'] > 70)
        sell_conditions.append(qtpylib.crossed_below(dataframe['ema_fast'], dataframe['ema_slow']))
        sell_conditions.append(dataframe['rsi'] < 30)

        if sell_conditions:
            dataframe.loc[
                (pd.concat(sell_conditions, axis=1)).any(axis=1),
                'exit_long'] = 1
            self.send_telegram_message(f"Sell signal detected for {metadata['pair']}!")

        return dataframe