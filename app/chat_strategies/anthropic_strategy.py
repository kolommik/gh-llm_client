"""
Implements the AnthropicChatStrategy, a concrete strategy for interacting with the Anthropic chat model API.
This strategy adheres to the ChatModelStrategy interface and encapsulates Anthropic-specific functionality.
"""

from anthropic import Anthropic
from chat_strategies.chat_model_strategy import ChatModelStrategy
from chat_strategies.model import Model


# https://docs.anthropic.com/claude/docs/models-overview
class AnthropicChatStrategy(ChatModelStrategy):
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            Model(
                name="claude-3-opus-20240229",
                output_max_tokens=4096,
                price_input=15.0,
                price_output=75.0,
            ),
            Model(
                name="claude-3-sonnet-20240229",
                output_max_tokens=4096,
                price_input=3.0,
                price_output=15.0,
            ),
            Model(
                name="claude-3-haiku-20240307",
                output_max_tokens=4096,
                price_input=0.25,
                price_output=1.25,
            ),
        ]
        self.client = Anthropic(api_key=self.api_key)
        self.input_tokens = 0
        self.output_tokens = 0
        self.model = None

    def get_models(self):
        return [model.name for model in self.models]

    def get_output_max_tokens(self, model_name) -> int:
        return self.models[self.get_models().index(model_name)].output_max_tokens

    def get_input_tokens(self):
        return self.input_tokens

    def get_output_tokens(self):
        return self.output_tokens

    def get_full_price(self) -> float:
        inputs = (
            self.input_tokens
            * self.models[self.get_models().index(self.model)].price_input
            / 1_000_000.0
        )
        outputs = (
            self.output_tokens
            * self.models[self.get_models().index(self.model)].price_output
            / 1_000_000.0
        )
        return inputs + outputs

    def send_message(
        self, system_prompt, messages, model_name, max_tokens, temperature=0
    ) -> str:

        self.model = model_name

        response = self.client.messages.create(
            model=model_name,
            messages=messages,
            system=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
        )

        self.input_tokens = response.usage.input_tokens
        self.output_tokens = response.usage.output_tokens

        return response.content[0].text
