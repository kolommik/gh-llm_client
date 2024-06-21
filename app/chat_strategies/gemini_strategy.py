"""
Implements the GeminiChatStrategy, a concrete strategy for interacting with the Google Gemini chat model API.
This strategy adheres to the ChatModelStrategy interface and encapsulates Gemini-specific functionality.
"""

from typing import List, Dict
import google.generativeai as genai
from chat_strategies.chat_model_strategy import ChatModelStrategy
from chat_strategies.model import Model


class GeminiChatStrategy(ChatModelStrategy):
    """
    A concrete strategy for interacting with the Google Gemini chat model API.

    Parameters
    ----------
    api_key : str
        The API key for accessing the Google Gemini API.

    Attributes
    ----------
    api_key : str
        The API key for accessing the Google Gemini API.
    models : List[Model]
        A list of available Gemini models.
    client : genai.GenerativeModel
        The Gemini client instance for making API requests.
    input_tokens : int
        The number of input tokens used in the last API request.
    output_tokens : int
        The number of output tokens generated in the last API response.
    model : str
        The name of the model used in the last API request.

    Methods
    -------
    get_models()
        Returns a list of available model names.
    get_output_max_tokens(model_name)
        Returns the maximum number of output tokens for the specified model.
    get_input_tokens()
        Returns the number of input tokens used in the last API request.
    get_output_tokens()
        Returns the number of output tokens generated in the last API response.
    get_full_price()
        Calculates and returns the total price based on the input and output tokens.
    send_message(system_prompt, messages, model_name, max_tokens, temperature)
        Sends a message to the Gemini API and returns the generated response.
    """

    # Gemini 1.5 Pro - models/gemini-1.5-pro
    # Price (input)
    # $3.50 / 1 million tokens (for prompts up to 128K tokens)
    # $7.00 / 1 million tokens (for prompts longer than 128K)
    # Price (output)
    # $10.50 / 1 million tokens (for prompts up to 128K tokens)
    # $21.00 / 1 million tokens (for prompts longer than 128K)

    # Gemini 1.5 Flash - models/gemini-1.5-flash
    # Price (input)
    # $0.35 / 1 million tokens (for prompts up to 128K tokens)
    # $0.70 / 1 million tokens (for prompts longer than 128K)
    # Price (output)
    # $1.05 / 1 million tokens (for prompts up to 128K tokens)
    # $2.10 / 1 million tokens (for prompts longer than 128K)
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.models = [
            Model(
                name="gemini-1.5-pro",
                output_max_tokens=8192,
                price_input=3.5,
                price_output=10.5,
            ),
            Model(
                name="gemini-1.5-flash",
                output_max_tokens=8192,
                price_input=0.35,
                price_output=1.05,
            ),
        ]

        self.client = None
        self.input_tokens = 0
        self.output_tokens = 0
        self.model = None

    def get_models(self) -> List[str]:
        return [model.name for model in self.models]

    def get_output_max_tokens(self, model_name: str) -> int:
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
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        model_name: str,
        max_tokens: int,
        temperature: float = 0,
    ) -> str:
        self.model = model_name
        self.client = genai.GenerativeModel(model_name)

        chat = self.client.start_chat(history=[])

        # Add system prompt
        chat.send_message(system_prompt)

        # Add previous messages
        for message in messages:
            chat.send_message(message["content"])

        # Send the last user message and get the response
        response = chat.send_message(
            messages[-1]["content"],
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens, temperature=temperature
            ),
        )

        self.input_tokens = response.usage_metadata.prompt_token_count
        self.output_tokens = response.usage_metadata.candidates_token_count

        return response.text
