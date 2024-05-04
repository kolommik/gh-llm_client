import os
import json
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from managers.file_manager import FileManager
from managers.log_manager import LogManager
from managers.settings_manager import SettingsManager
from managers.chat_history_manager import ChatHistoryManager
from chat_strategies.openai_strategy import OpenAIChatStrategy
from chat_strategies.anthropic_strategy import AnthropicChatStrategy
from utils.constants import MODELS_TABLE


DIVIDER = ": "


class StreamlitInterface:
    def __init__(
        self,
        settings_manager,
        log_manager,
        chat_history_manager,
        openai_api_key=None,
        anthropic_api_key=None,
    ):
        self.settings_manager = settings_manager
        self.log_manager = log_manager
        self.chat_history_manager = chat_history_manager

        # TODO - обработка ошибки если список моделей пуст, т.к. нет env ключей

        self.strategies = {
            "OpenAI": (
                OpenAIChatStrategy(api_key=openai_api_key) if openai_api_key else None
            ),
            "Anthropic": (
                AnthropicChatStrategy(api_key=anthropic_api_key)
                if anthropic_api_key
                else None
            ),
        }

        self.models_list = []
        for strategy_name, strategy in self.strategies.items():
            if strategy:
                self.models_list.extend(
                    [
                        f"{strategy_name}{DIVIDER}{model}"
                        for model in strategy.get_models()
                    ]
                )

    def run(self):
        # ===========================================================
        # Настройки
        st.sidebar.title("Настройки")

        # Загрузка и сохранение настроек
        settings = self.settings_manager.load_settings()

        folder_path = st.sidebar.text_input(
            "Folder path",
            settings.get("folder_path", ""),
            help="Введите путь к директории",
        )
        target_extensions = st.sidebar.text_input(
            "Target extensions",
            settings.get("target_extensions", ""),
            help="Введите расширения через запятую, например: .py,.txt,.md",
        )
        always_include = st.sidebar.text_input(
            "Always include files",
            settings.get("always_include", ""),
            help="Введите имена файлов через запятую",
        )
        excluded_dirs = st.sidebar.text_input(
            "Excluded directories",
            settings.get("excluded_dirs", ""),
            help="Введите директории через запятую",
        )
        system_prompt = st.sidebar.text_area(
            "System prompt", settings.get("system_prompt", "")
        )

        if st.sidebar.button("Сохранить настройки"):
            new_settings = {
                "folder_path": folder_path,
                "target_extensions": target_extensions,
                "always_include": always_include,
                "excluded_dirs": excluded_dirs,
                "system_prompt": system_prompt,
            }
            self.settings_manager.save_settings(new_settings)
            st.success("Настройки сохранены!")
            settings = new_settings

        if st.sidebar.button("Загрузить настройки"):
            settings = self.settings_manager.load_settings()
            st.success("Настройки загружены!")

        st.sidebar.write("---")

        chosen_model = st.sidebar.selectbox(
            "Model name",
            (self.models_list),
            help="Выберите модель из доступных",
        )

        self.current_strategy, self.current_model = chosen_model.split(DIVIDER)
        self.output_max_tokens = self.strategies[
            self.current_strategy
        ].get_output_max_tokens(self.current_model)

        current_model_details = [
            item for item in MODELS_TABLE if item["name"] == self.current_model
        ]

        temperature = st.sidebar.slider(
            "Temperature",
            0.0,
            1.0,
            0.0,
            help="""
            Параметр, контролирующий случайность ответов модели.
            Значение 0 означает, что модель будет генерировать более предсказуемый и консистентный текст.""",
        )
        # max_tokens = st.sidebar.number_input(
        #     "Max tokens",
        #     min_value=1000,
        #     max_value=MAX_TOKENS,
        #     value=MAX_TOKENS,
        #     step=50,
        #     help="""
        #     Максимальное количество токенов, которое может быть сгенерировано в ответе.
        #     Это помогает ограничить длину вывода.""",
        # )

        # ===========================================================
        # Основной интерфейс
        context_tab, chat_tab, log_tab, model_tab = st.tabs(
            ["Контекст", "💬 Чат", "Лог", "LLM Модель"]
        )

        with model_tab:
            st.table(MODELS_TABLE)

            st.write("---")

            if current_model_details:
                with st.expander("Current model", expanded=True):
                    st.write(current_model_details)

        # Контекст ==================================================
        with context_tab:
            if st.button("Обновить контекст"):
                file_manager = FileManager(
                    folder_path=folder_path,
                    target_extensions=target_extensions,
                    always_include=always_include,
                    excluded_dirs=excluded_dirs,
                )

                files = file_manager.read_files()
                st.session_state["context"] = files

            if "context" in st.session_state:
                st.write(
                    "Total tokens:",
                    sum([x["tokens"] for x in st.session_state["context"]]),
                )
                st.table(
                    [
                        {
                            "path": item["path"],
                            "tokens": item["tokens"],
                            "length (bytes)": item["length"],
                        }
                        for item in st.session_state["context"]
                    ]
                )

            with st.expander("System prompt", expanded=False):
                st.text(system_prompt)

            if "context" in st.session_state:
                with st.expander("Files data", expanded=False):
                    st.write(st.session_state["context"])

        # Чат =======================================================
        with chat_tab:

            if st.button("Очистить историю чата"):
                st.session_state["messages"] = []

            if st.button("Сохранить чат"):
                filepath = self.chat_history_manager.save_chat_history(
                    st.session_state.messages
                )
                st.success(f"Чат сохранен в файл: {filepath}")

            if st.button("Загрузить чат"):
                st.warning("Заглушка. Не реализовано")

            if "messages" not in st.session_state:
                st.session_state["messages"] = []

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input():
                if not self.current_strategy:
                    st.info(
                        "Please add your API key to continue. [OpenAI or Anthropic]"
                    )
                    st.stop()

                st.session_state.messages.append(
                    {"role": "user", "content": f"Question: {prompt}"}
                )
                # st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)

                context_str = ""
                if "context" in st.session_state:
                    for item in st.session_state["context"]:
                        context_str += "LOCAL FILEPATH: " + item["path"] + "\n"
                        context_str += "CONTENTS:\n" + item["content"] + "\n\n"

                messages_with_context = []

                if len(context_str) > 0:
                    messages_with_context.extend(
                        [
                            {"role": "user", "content": f"Context:\n\n{context_str}"},
                            {"role": "assistant", "content": "Ok, I got it!"},
                        ]
                    )

                messages_with_context.extend(st.session_state.messages.copy())

                msg = self.strategies[self.current_strategy].send_message(
                    system_prompt=system_prompt,
                    messages=messages_with_context,
                    model_name=self.current_model,
                    max_tokens=self.output_max_tokens,
                    temperature=temperature,
                )

                # input_tokens = self.strategies[self.current_strategy].get_input_tokens()
                # output_tokens = self.strategies[
                #     self.current_strategy
                # ].get_output_tokens()
                # total_price = self.strategies[self.current_strategy].get_full_price()

                # st.write(
                #     [
                #         f"input_tokens: {input_tokens},output_tokens: {output_tokens}.",
                #         f" Price: {total_price} $ (~{total_price*100:,.3} Rub)",
                #     ]
                # )

                self.log_manager.add_log(
                    f"{self.current_strategy} - {self.current_model}"
                )

                st.session_state.messages.append({"role": "assistant", "content": msg})
                with st.chat_message("assistant"):
                    st.write(msg)

                self.log_manager.add_log(f"{self.strategies[self.current_strategy]}")
                self.log_manager.add_log("=" * 40)
                self.log_manager.add_log(messages_with_context)

                self.log_manager.add_log(
                    json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
                )
                self.log_manager.add_log("=" * 40)
                self.log_manager.add_log("Ответ ассистента отправлен.")
                self.log_manager.add_log(msg)

        # Логи ======================================================
        with log_tab:
            st.write(st.session_state)
            # st.session_state.get("log", [])
            with st.expander("Лог системы", expanded=True):
                st.text("\n".join(self.log_manager.get_logs()))


if __name__ == "__main__":
    load_dotenv(find_dotenv())  # read local.env file
    openai_api_key = os.environ["OPENAI_API_KEY"]
    anthropic_api_key = os.environ["ANTHROPIC_API_KEY"]

    settings_manager = SettingsManager()
    log_manager = LogManager()
    chat_history_manager = ChatHistoryManager()

    app = StreamlitInterface(
        settings_manager,
        log_manager,
        chat_history_manager,
        openai_api_key,
        anthropic_api_key,
    )
    app.run()
