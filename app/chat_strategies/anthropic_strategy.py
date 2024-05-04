from anthropic import Anthropic
from chat_strategies.chat_model_strategy import ChatModelStrategy
from chat_strategies.model import Model


# https://docs.anthropic.com/claude/docs/models-overview
class AnthropicChatStrategy(ChatModelStrategy):
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            Model(name="claude-3-opus-20240229", output_max_tokens=4096),
            Model(name="claude-3-sonnet-20240229", output_max_tokens=4096),
            Model(name="claude-3-haiku-20240307", output_max_tokens=4096),
        ]
        self.client = Anthropic(api_key=self.api_key)

    def get_models(self):
        return [model.name for model in self.models]

    def get_output_max_tokens(self, model_name) -> int:
        return self.models[self.get_models().index(model_name)].output_max_tokens

    def send_message(
        self, system_prompt, messages, model_name, max_tokens, temperature=0
    ) -> str:

        response = self.client.messages.create(
            model=model_name,
            messages=messages,
            system=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
        )

        return response.content[0].text, response
