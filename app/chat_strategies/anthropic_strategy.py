from chat_strategies.chat_model_strategy import ChatModelStrategy
from chat_strategies.model import Model

# TODO Сделать отдельную стратегию отправки сообщения через Antropic


class AnthropicChatStrategy(ChatModelStrategy):
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            Model(name="Haiku"),
            Model(name="Opus"),
        ]

    def get_models(self):
        return [model.name for model in self.models]

    def send_message(self, messages, model_name) -> str:
        # Логика отправки сообщения через Antropic
        return "Ответ от Antropic"
