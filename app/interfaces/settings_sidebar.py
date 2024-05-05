import streamlit as st

DIVIDER = ": "


class SettingsSidebar:
    def __init__(self, settings_manager, strategies):
        self.settings_manager = settings_manager
        self.strategies = strategies

        self.models_list = []
        for strategy_name, strategy in self.strategies.items():
            if strategy:
                self.models_list.extend(
                    [
                        f"{strategy_name}{DIVIDER}{model}"
                        for model in strategy.get_models()
                    ]
                )

    def render(self):
        st.sidebar.title("Настройки")

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

        return settings, current_strategy, current_model, temperature, max_tokens
