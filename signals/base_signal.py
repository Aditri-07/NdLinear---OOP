# signals/base_signal.py

from abc import ABC, abstractmethod

class BaseSignal(ABC):
    """
    Abstract Base Class for all types of signals.
    """

    @abstractmethod
    def calculate_signal(self):
        """
        Calculate the signal.
        Must be implemented by all subclasses.
        """
        pass
