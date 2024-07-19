"""
Implements the OpenAIChatStrategy, a concrete strategy for interacting with the OpenAI chat model API.
This strategy adheres to the ChatModelStrategy interface and encapsulates OpenAI-specific functionality.
"""

from typing import List, Dict
from openai import OpenAI
from chat_strategies.model import Model
from chat_strategies.chat_model_strategy import ChatModelStrategy


# https://platform.openai.com/docs/models
# https://openai.com/pricing#language-models
class OpenAIChatStrategy(ChatModelStrategy):
    """
    A concrete strategy for interacting with the OpenAI chat model API.

    Parameters
    ----------
    api_key : str
        The API key for accessing the OpenAI API.

    Attributes
    ----------
    api_key : str
        The API key for accessing the OpenAI API.
    models : List[Model]
        A list of available OpenAI models.
    client : OpenAI
        The OpenAI client instance for making API requests.
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
        Sends a message to the OpenAI API and returns the generated response.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.models = [
            Model(
                name="gpt-4o",
                output_max_tokens=4096,
                price_input=5.0,
                price_output=15.0,
            ),
            Model(
                name="gpt-4o-mini",
                output_max_tokens=4096,
                price_input=0.15,
                price_output=0.6,
            ),
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
        ]
        self.client = OpenAI(api_key=self.api_key)
        self.input_tokens = 0
        self.output_tokens = 0
        self.model = None

    def get_models(self) -> List[str]:
        """
        Returns a list of available model names.

        Returns
        -------
        List[str]
            A list of available model names.
        """
        return [model.name for model in self.models]

    def get_output_max_tokens(self, model_name: str) -> int:
        """
        Returns the maximum number of output tokens for the specified model.

        Parameters
        ----------
        model_name : str
            The name of the model.

        Returns
        -------
        int
            The maximum number of output tokens for the specified model.
        """
        return self.models[self.get_models().index(model_name)].output_max_tokens

    def get_input_tokens(self) -> int:
        """
        Returns the number of input tokens used in the last API request.

        Returns
        -------
        int
            The number of input tokens used in the last API request.
        """
        return self.input_tokens

    def get_output_tokens(self) -> int:
        """
        Returns the number of output tokens generated in the last API response.

        Returns
        -------
        int
            The number of output tokens generated in the last API response.
        """
        return self.output_tokens

    def get_full_price(self) -> float:
        """
        Calculates and returns the total price based on the input and output tokens.

        Returns
        -------
        float
            The total price based on the input and output tokens.
        """
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
        """Sends a message to the OpenAI API and returns the generated response.

        Parameters
        ----------
        system_prompt : str
            The system prompt to provide context for the conversation.
        messages : List[Dict[str, str]]
            A list of messages in the conversation, each represented as a dictionary.
        model_name : str
            The name of the model to use for generating the response.
        max_tokens : int
            The maximum number of tokens to generate in the response.
        temperature : float, optional
            The temperature value to control the randomness of the generated response, by default 0.

        Returns
        -------
        str
            The generated response from the OpenAI API.
        """
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
