from abc import ABC, abstractmethod

class BrokerBase(ABC):
    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def place_order(self, symbol, qty, action):
        pass

    @abstractmethod
    def get_positions(self):
        pass
