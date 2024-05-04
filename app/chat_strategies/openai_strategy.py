from openai import OpenAI
from chat_strategies.model import Model
from chat_strategies.chat_model_strategy import ChatModelStrategy


# https://platform.openai.com/docs/models
# https://openai.com/pricing#language-models
class OpenAIChatStrategy(ChatModelStrategy):
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            Model(
                name="gpt-4-turbo",
                output_max_tokens=4096,
                price_input=10.0,
                price_output=30.0,
            ),
            Model(
                name="gpt-3.5-turbo",
                output_max_tokens=4096,
                price_input=0.5,
                price_output=1.5,
            ),
            Model(
                name="gpt-4",
                output_max_tokens=4096,
                price_input=30.0,
                price_output=60.0,
            ),
            Model(
                name="gpt-4-32k",
                output_max_tokens=4096,
                price_input=60.0,
                price_output=120.0,
            ),
        ]
        self.client = OpenAI(api_key=self.api_key)
        self.input_tokens = 0
        self.output_tokens = 0
        self.model = None

    def get_models(self):
        return [model.name for model in self.models]

    def get_output_max_tokens(self, model_name) -> int:
        return self.models[self.get_models().index(model_name)].output_max_tokens

    def get_input_tokens(self) -> int:
        return self.input_tokens

    def get_output_tokens(self) -> int:
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

        full_messages = [{"role": "system", "content": f"{system_prompt}"}]
        full_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=model_name,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        self.input_tokens = response.usage.prompt_tokens
        self.output_tokens = response.usage.completion_tokens

        return response.choices[0].message.content
