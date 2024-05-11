"""
Implements the settings sidebar in the Streamlit app, allowing users to modify and save settings,
as well as select the desired chat model and its parameters.
"""

from typing import Dict, Tuple
import streamlit as st
import json

from chat_strategies.chat_model_strategy import ChatModelStrategy
from managers.settings_manager import SettingsManager

DIVIDER = ": "


class SettingsSidebar:
    def __init__(
        self,
        settings_manager: SettingsManager,
        strategies: Dict[str, ChatModelStrategy],
    ):

        self.settings_manager = settings_manager
        self.strategies = strategies
        self.models_list = self._create_models_list()
        self.output_max_tokens: int = 0

    def _create_models_list(self) -> None:
        models_list = []
        for strategy_name, strategy in self.strategies.items():
            if strategy:
                models_list.extend(
                    [
                        f"{strategy_name}{DIVIDER}{model}"
                        for model in strategy.get_models()
                    ]
                )
        return models_list

    def _handle_settings(self) -> None:
        if "settings" not in st.session_state:
            st.session_state["settings"] = self.settings_manager.load_settings()

        if st.sidebar.button("Сохранить настройки по умолчанию"):
            new_settings = {
                "folder_path": st.session_state.settings["folder_path"],
                "target_extensions": st.session_state.settings["target_extensions"],
                "always_include": st.session_state.settings["always_include"],
                "excluded_dirs": st.session_state.settings["excluded_dirs"],
                "system_prompt": st.session_state.settings["system_prompt"],
            }
            self.settings_manager.save_settings(new_settings)
            st.sidebar.success("Настройки сохранены!")

            # Предложить скачать файл с настройками
            settings_json = json.dumps(new_settings, ensure_ascii=False, indent=2)
            st.sidebar.download_button(
                label="Скачать файл настроек",
                data=settings_json,
                file_name="settings.json",
                mime="application/json",
            )

        if st.sidebar.button("Загрузить настройки по умолчанию"):
            st.session_state["settings"] = self.settings_manager.load_settings()
            st.sidebar.success("Настройки загружены!")

        settings_file = st.sidebar.file_uploader(
            "Выберите файл настроек",
            type=["json"],
            help="Загрузить локальный файл JSON с настройками",
        )

        if settings_file is not None:
            st.session_state["settings"] = (
                self.settings_manager.load_settings_from_file(settings_file)
            )
            st.sidebar.success(f"Настройки загружены из файла {settings_file.name}!")

    def render(self) -> Tuple[str, str, float, int]:
        st.sidebar.title("Настройки")
        self._handle_settings()

        unique_key = hash(json.dumps(st.session_state["settings"], sort_keys=True))

        # -----------------------------------------------
        st.sidebar.write("---")

        st.session_state.settings["folder_path"] = st.sidebar.text_input(
            "Folder path",
            st.session_state.settings.get("folder_path", ""),
            key=f"folder_path_{unique_key}",
            help="Введите путь к директории",
        )
        st.session_state.settings["target_extensions"] = st.sidebar.text_input(
            "Target extensions",
            st.session_state.settings.get("target_extensions", ""),
            key=f"target_extensions_{unique_key}",
            help="Введите расширения через запятую, например: .py,.txt,.md",
        )
        st.session_state.settings["always_include"] = st.sidebar.text_input(
            "Always include files",
            st.session_state.settings.get("always_include", ""),
            key=f"always_include_{unique_key}",
            help="Введите имена файлов через запятую",
        )
        st.session_state.settings["excluded_dirs"] = st.sidebar.text_input(
            "Excluded directories",
            st.session_state.settings.get("excluded_dirs", ""),
            key=f"excluded_dirs_{unique_key}",
            help="Введите директории через запятую",
        )
        st.session_state.settings["system_prompt"] = st.sidebar.text_area(
            "System prompt",
            st.session_state.settings.get("system_prompt", ""),
            key=f"system_prompt_{unique_key}",
            help="Системная подсказка для LLM",
        )

        st.sidebar.write("---")

        chosen_model = st.sidebar.selectbox(
            "Model name",
            (self.models_list),
            help="Выберите модель из доступных",
        )

        current_strategy, current_model = chosen_model.split(DIVIDER)
        self.output_max_tokens = self.strategies[
            current_strategy
        ].get_output_max_tokens(current_model)

        temperature = st.sidebar.slider(
            "Temperature",
            0.0,
            1.0,
            0.0,
            help="""
            Параметр, контролирующий случайность ответов модели.
            Значение 0 означает, что модель будет генерировать более предсказуемый и консистентный текст.""",
        )
        max_tokens = st.sidebar.number_input(
            "Max tokens",
            min_value=1000,
            max_value=self.output_max_tokens,
            value=self.output_max_tokens,
            step=100,
            help="""
            Максимальное количество токенов, которое может быть сгенерировано в ответе.
            Это помогает ограничить длину вывода.""",
        )

        return current_strategy, current_model, temperature, max_tokens
