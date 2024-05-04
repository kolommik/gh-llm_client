MAX_TOKENS = 4096

# https://platform.openai.com/docs/models
# https://openai.com/pricing#language-models
MODELS_TABLE = [
    {
        "name": "gpt-3.5-turbo",
        "context": "16'383",
        "output": "4'096",
        "last_update": "2021-09",
        "price input": "$0.5 - 1M tokens",
        "price output": "$1.5 - 1M tokens",
        "input_price": 0.5,
        "output_price": 1.5,
        "points on": "gpt-3.5-turbo-0125",
    },
    {
        "name": "gpt-4-turbo",
        "context": "128'000",
        "output": "4'096",
        "last_update": "2023-12",
        "price input": "$10 - 1M tokens",
        "price output": "$30 - 1M tokens",
        "input_price": 10.0,
        "output_price": 30.0,
        "points on": "gpt-4-turbo-2024-04-09 (v5)",
    },
    {
        "name": "gpt-4",
        "context": "8'192",
        "output": "4'096",
        "last_update": "2021-09",
        "price input": "$30 - 1M tokens",
        "price output": "$60 - 1M tokens",
        "input_price": 30.0,
        "output_price": 60.0,
        "points on": "gpt-4-0613",
    },
    {
        "name": "gpt-4-32k",
        "context": "32'768",
        "output": "4'096",
        "last_update": "2021-09",
        "price input": "$60 - 1M tokens",
        "price output": "$120 - 1M tokens",
        "input_price": 60.0,
        "output_price": 120.0,
        "points on": "gpt-4-32k-0613",
    },
]
