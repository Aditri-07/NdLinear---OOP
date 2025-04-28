import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class SimpleBacktester:
    def __init__(self, data, strategy):
        self.data = self.data = data
        self.strategy = strategy
        self.initial_cash = 10000
        self.portfolio_values = []   

    def run_backtest(self):
        cash = self.initial_cash
        position = 0
        self.trades = []

        self.data = self.strategy.generate_signals(self.data)

        for idx, row in self.data.iterrows():
            price = row['Close']
            signal = row['Signal']

            if signal == 'buy' and cash >= price:
                buy_price = price
                position += cash / price
                cash = 0

            elif signal == 'sell' and position > 0:
                sell_price = price
                cash += position * price
                self.trades.append((buy_price, sell_price))
                position = 0

            portfolio_today = cash + position * price
            self.portfolio_values.append(portfolio_today)  

        return self.data

    def plot_performance(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,6))
        plt.plot(self.portfolio_values)
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Days')
        plt.ylabel('Portfolio Value')
        plt.grid()
        plt.show()

    def calculate_performance_metrics(self):
        portfolio_series = pd.Series(self.portfolio_values)
        returns = portfolio_series.pct_change().dropna()

        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()

        print(f"Performance Metrics:")
        print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
        print(f"Maximum Drawdown: {max_drawdown:.2%}")

    def calculate_trade_statistics(self):
        if not hasattr(self, 'trades') or not self.trades:
            print("No trades recorded.")
            return

        profits = [sell - buy for buy, sell in self.trades]
        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p <= 0]

        win_rate = len(wins) / len(profits) if profits else 0
        avg_profit = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses) if losses else 0

        print(f"Trade Statistics:")
        print(f"Win Rate: {win_rate:.2%}")
        print(f"Average Profit on Wins: {avg_profit:.2f}")
        print(f"Average Loss on Losses: {avg_loss:.2f}")
