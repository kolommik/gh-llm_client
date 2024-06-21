# Installation Guide

[English](INSTALLATION.md) | [Русский](../ru/INSTALLATION.md)

## Requirements

- Python 3.10 or higher
- Poetry

## Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/kolommik/gh-llm_client.git
    cd my-streamlit-app
    ```

2. **Install dependencies:**

    ```sh
    poetry install
    ```

3. **Set up environment variables:**

    Create a `.env` file in the root directory and add your API keys:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ANTHROPIC_API_KEY=your_anthropic_api_key
    GOOGLE_API_KEY = your_google_api_key    
    ```

4. **Run the application:**

    ```sh
    poetry run streamlit run app/main.py
    ```

## Additional Information

For more details on how to use the application, see [USAGE.md](USAGE.md).