"""
This module implements the Strategy pattern for interacting with different chat model APIs.

Defines the ChatModelStrategy abstract base class, which serves as the common interface for all chat model strategies.
This class enforces the implementation of essential methods for interacting with chat model APIs.

Guidelines for refactoring and extending this module:
1. Adhere to the Strategy pattern
2. Avoid coupling the strategies with the client code
3. Keep the strategies focused and cohesive
4. Consider extracting common functionality
5. Maintain the interface of `ChatModelStrategy`

Following these guidelines will keep the module flexible, extensible, and aligned with the Strategy pattern.
"""

from typing import List, Dict
from abc import ABC, abstractmethod


class ChatModelStrategy(ABC):
    @abstractmethod
    def get_models(self) -> List[str]:
        """Returns a list of available models for a strategy"""
        pass

    @abstractmethod
    def get_output_max_tokens(self, model_name: str) -> int:
        """Returns maximum output tokens limit"""
        pass

    @abstractmethod
    def get_input_tokens(self) -> int:
        """Returns input tokens count"""
        pass

    @abstractmethod
    def get_output_tokens(self) -> int:
        """Returns output tokens count"""
        pass

    @abstractmethod
    def get_full_price(self) -> float:
        """Returns the cost"""
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
