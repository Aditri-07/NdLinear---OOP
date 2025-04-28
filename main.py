import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'NdLinear', 'src', 'ndlinear'))

from signals.technical_signal import RSISignal
from backtester.backtester import SimpleBacktester
from strategy.ndlinear_strategy import NdLinearStrategy
import torch
import pandas as pd
import numpy as np
import random
torch.manual_seed(42)
np.random.seed(42)
random.seed(42)

# Step 1: Fetch price data and calculate RSI
rsi_signal = RSISignal('NVDA', start_date='2020-01-01', end_date='2025-01-01')
rsi_values = rsi_signal.calculate_signal()
data_with_rsi = rsi_signal.get_data_with_rsi()

# ⚡ CRUCIAL: Flatten the columns if multi-indexed
# Fix multi-index or weird columns
if isinstance(data_with_rsi.columns, pd.MultiIndex):
    data_with_rsi.columns = data_with_rsi.columns.get_level_values(-1)

# Rename columns properly
data_with_rsi.columns = ['Close', 'High', 'Low', 'Open', 'Volume', 'RSI']


print("Data with RSI:\n", data_with_rsi.tail())

# Step 2: Initialize strategy
ndlinear_strategy = NdLinearStrategy()

# Step 3: Initialize backtester
backtester = SimpleBacktester(data_with_rsi, ndlinear_strategy)
backtest_results = backtester.run_backtest()
backtester.plot_performance()
backtester.calculate_performance_metrics()
backtester.calculate_trade_statistics()

