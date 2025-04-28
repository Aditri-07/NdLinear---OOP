# signals/ndlinear_signal.py

import torch
from torch import nn
from NdLinear.ndlinear import NdLinear
from signals.base_signal import BaseSignal

class NdLinearSignal(BaseSignal):
    """
    A class to apply NdLinear transformation on technical indicators.
    """

    def __init__(self, input_array, input_shape, hidden_shape):
        """
        input_array: a numpy array or tensor of technical signals (e.g., RSI values)
        input_shape: tuple, shape of input (e.g., (n_samples, 1))
        hidden_shape: tuple, desired shape after transformation
        """
        self.input_array = input_array
        self.input_shape = input_shape
        self.hidden_shape = hidden_shape

        self.model = NdLinear(input_dims=self.input_shape, hidden_size=self.hidden_shape)

    def calculate_signal(self):
        """
        Apply NdLinear transformation and return the output tensor.
        """
        if not isinstance(self.input_array, torch.Tensor):
            input_tensor = torch.tensor(self.input_array, dtype=torch.float32)
        else:
            input_tensor = self.input_array

        output_tensor = self.model(input_tensor)
        return output_tensor
