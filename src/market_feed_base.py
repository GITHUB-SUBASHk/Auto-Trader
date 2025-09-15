from abc import ABC, abstractmethod

class MarketFeedBase(ABC):
    @abstractmethod
    def start(self):
        pass
