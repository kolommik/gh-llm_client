from openai import OpenAI
from chat_strategies.model import Model
from chat_strategies.chat_model_strategy import ChatModelStrategy

MAX_TOKENS = 4096


class OpenAIChatStrategy(ChatModelStrategy):
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            Model(name="gpt-4-turbo"),
            Model(name="gpt-3.5-turbo"),
            Model(name="gpt-4"),
            Model(name="gpt-4-32k"),
        ]
        self.client = OpenAI(api_key=self.api_key)

    def get_models(self):
        return [model.name for model in self.models]

    def send_message(self, messages, model_name) -> str:
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0,
            max_tokens=MAX_TOKENS,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content
