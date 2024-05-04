from typing import List, Dict
from abc import ABC, abstractmethod


class ChatModelStrategy(ABC):
    @abstractmethod
    def get_models(self) -> List[str]:
        """Возвращает список доступных моделей для стратегии."""
        pass

    @abstractmethod
    def get_output_max_tokens(self, model_name) -> int:
        """Возвращает максимальное количество токенов для выбранной модели"""
        pass

    @abstractmethod
    def get_input_tokens(self) -> int:
        """Возвращает использованное количество токенов для ввода"""
        pass

    @abstractmethod
    def get_output_tokens(self) -> int:
        """Возвращает использованное количество токенов для вывода"""
        pass

    @abstractmethod
    def get_full_price(self) -> float:
        """Возвращает стоимость диалога"""
        pass

    @abstractmethod
    def send_message(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        model_name: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        pass
