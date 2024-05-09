"""
Defines the Model class, which represents a chat model with its associated properties such as name, output_max_tokens,
price_input, and price_output.
This class is used by the chat model strategies to store and access model-specific information.
"""


class Model:
    def __init__(
        self, name: str, output_max_tokens: int, price_input: float, price_output: float
    ):
        self.name = name
        self.output_max_tokens = output_max_tokens
        self.price_input = price_input
        self.price_output = price_output
