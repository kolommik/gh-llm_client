from chat_strategies.chat_model_strategy import ChatModelStrategy

# TODO Сделать отдельную стратегию отправки сообщения через локальную LLAMA


class LLAMAStrategy(ChatModelStrategy):
    def send_message(self, message: str) -> str:
        # Логика отправки сообщения через локальную LLAMA модель
        return "Ответ от локальной модели"
