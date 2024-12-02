from abc import ABC, abstractmethod

class Subscriber(ABC):
    @abstractmethod
    def on_message(message):
        pass
