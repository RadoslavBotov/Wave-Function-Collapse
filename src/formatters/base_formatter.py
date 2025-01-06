from abc import ABC, abstractmethod


class Formatter(ABC):
    
    @abstractmethod
    def format_item(cls, configs: dict) -> dict:
        pass
