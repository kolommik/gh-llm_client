# Руководство по установке

[English](../en/INSTALLATION.md) | [Русский](INSTALLATION.md)

## Требования

- Python 3.10 или выше
- Poetry

## Шаги

1. **Клонируйте репозиторий:**

    ```sh
    git clone https://github.com/kolommik/gh-llm_client.git
    cd my-streamlit-app
    ```

2. **Установите зависимости:**

    ```sh
    poetry install
    ```

3. **Настройте переменные окружения:**

    Создайте файл `.env` в корневом каталоге и добавьте свои API ключи:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ANTHROPIC_API_KEY=your_anthropic_api_key
    GOOGLE_API_KEY = your_google_api_key
    ```

4. **Запустите приложение:**

    ```sh
    poetry run streamlit run app/main.py
    ```

## Дополнительная информация

Для получения более подробной информации о том, как использовать приложение, см. [USAGE.md](USAGE.md).