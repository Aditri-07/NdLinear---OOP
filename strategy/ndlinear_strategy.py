# strategy/ndlinear_strategy.py

# strategy/ndlinear_strategy.py

import torch
import numpy as np
from strategy.base_strategy import BaseStrategy
from NdLinear.ndlinear import NdLinear
torch.manual_seed(42)

class NdLinearStrategy(BaseStrategy):
    def __init__(self, input_shape=(1,), hidden_shape=(2,)):
        self.model = NdLinear(input_dims=input_shape, hidden_size=hidden_shape)
        for layer in self.model.align_layers:
            layer.weight.data *= 10
            layer.bias.data *= 10
        
    def generate_signals(self, data):
        """
        For each day:
        - take today's RSI
        - transform using NdLinear
        - decide buy/sell/hold
        """
        data = data.copy()  # Avoid SettingWithCopyWarning

        signals = []
        last_signal = 'none'


        for idx, row in data.iterrows():
            rsi_value = (row['RSI'] - 50)  # Center RSI around 0
            if isinstance(rsi_value, (float, int, np.float32, np.float64)):
                rsi_value = float(rsi_value)
            else:
                rsi_value = float(rsi_value.iloc[0])
            
            # Pass each RSI value individually
            input_tensor = torch.tensor([[rsi_value]], dtype=torch.float32)
            transformed_output = self.model(input_tensor)
            output = transformed_output.detach().numpy()
            signal_value = output[0, 0]  # <<< take only the first output dimension
            
            #print(f"Day {idx}: RSI={rsi_value:.2f}, Transformed={signal_value:.4f}")

            if signal_value < -0.001:
                signals.append('buy')
            elif signal_value > 0.001:
                signals.append('sell')
            else:
                signals.append('hold')
            #print(signal_value, signals[-1])

        data['Signal'] = signals
        return data
        
   