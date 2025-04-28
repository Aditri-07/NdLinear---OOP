from strategy.base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def generate_signals(self, data):
        signals = []
        last_signal = 'none'

        for idx, row in data.iterrows():
            rsi = row['RSI']

            if rsi < 30 and last_signal != 'buy':
                signals.append('buy')
                last_signal = 'buy'
            elif rsi > 70 and last_signal == 'buy':
                signals.append('sell')
                last_signal = 'sell'
            else:
                signals.append('hold')

        data['Signal'] = signals
        return data
