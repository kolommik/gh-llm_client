from openai import OpenAI
from chat_strategies.model import Model
from chat_strategies.chat_model_strategy import ChatModelStrategy


# https://platform.openai.com/docs/models
# https://openai.com/pricing#language-models
class OpenAIChatStrategy(ChatModelStrategy):
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            Model(name="gpt-4-turbo", output_max_tokens=4096),
            Model(name="gpt-3.5-turbo", output_max_tokens=4096),
            Model(name="gpt-4", output_max_tokens=4096),
            Model(name="gpt-4-32k", output_max_tokens=4096),
        ]
        self.client = OpenAI(api_key=self.api_key)

    def get_models(self):
        return [model.name for model in self.models]

    def get_output_max_tokens(self, model_name) -> int:
        return self.models[self.get_models().index(model_name)].output_max_tokens

    def send_message(
        self, system_prompt, messages, model_name, max_tokens, temperature=0
    ) -> str:

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
        return response.choices[0].message.content, response
