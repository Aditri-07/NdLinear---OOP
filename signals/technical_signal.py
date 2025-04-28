# signals/technical_signal.py

import pandas as pd
import yfinance as yf
from signals.base_signal import BaseSignal

class RSISignal(BaseSignal):
    """
    A class to calculate the Relative Strength Index (RSI) signal.
    """

    def __init__(self, ticker, start_date, end_date, period=14):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.data = self._fetch_data()
        self.rsi = None  # will hold the RSI values after calculation

    def _fetch_data(self):
        """
        Fetch historical stock price data from Yahoo Finance.
        """
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return df

    def calculate_signal(self):
        """
        Calculate the RSI signal and store it.
        """
        delta = self.data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        self.rsi = 100 - (100 / (1 + rs))
        return self.rsi

    def get_data_with_rsi(self):
        """
        Return the dataframe with RSI attached.
        """
        if self.rsi is None:
            self.calculate_signal()
        df_with_rsi = self.data.copy()
        df_with_rsi['RSI'] = self.rsi
        return df_with_rsi
