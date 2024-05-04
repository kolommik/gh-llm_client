from typing import List, Dict
from abc import ABC, abstractmethod


class ChatModelStrategy(ABC):
    @abstractmethod
    def get_models(self) -> List[str]:
        """Возвращает список доступных моделей для стратегии."""
        pass

    @abstractmethod
    def send_message(self, messages: List[Dict[str, str]], model_name: str) -> str:
        pass
