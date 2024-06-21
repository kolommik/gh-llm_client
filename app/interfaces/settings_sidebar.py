"""
Implements the settings sidebar in the Streamlit app, allowing users to modify and save settings,
as well as select the desired chat model and its parameters.
"""

from typing import Dict, Tuple
import streamlit as st
import json
import os

from chat_strategies.chat_model_strategy import ChatModelStrategy
from managers.settings_manager import SettingsManager

DIVIDER = ": "


class SettingsSidebar:
    """Class representing the settings sidebar in the Streamlit app.

    Parameters
    ----------
    settings_manager : SettingsManager
        Instance of the SettingsManager class for managing settings.
    strategies : Dict[str, ChatModelStrategy]
        Dictionary mapping strategy names to ChatModelStrategy instances.

    Attributes
    ----------
    models_list : List[str]
        List of available chat models.
    output_max_tokens : int
        Maximum number of output tokens for the selected model.

    Methods
    -------
    render() -> Tuple[str, str, float, int]
        Renders the settings sidebar and returns the selected strategy, model, temperature, and max tokens.
    """

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
        """
        Creates a list of available chat models.
        """
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
        """
        Handles the settings in the sidebar, including loading, saving, and updating settings.
        """
        if "settings" not in st.session_state:
            st.session_state["settings"] = self.settings_manager.load_settings()

        settings_files = [f for f in os.listdir("settings") if f.endswith(".json")]
        selected_file = st.sidebar.selectbox(
            "Select settings file",
            settings_files,
            index=(
                settings_files.index("default_settings.json")
                if "default_settings.json" in settings_files
                else 0
            ),
        )

        if st.sidebar.button("Save settings"):
            # Save settings to the selected file
            new_settings = {
                "folder_path": st.session_state.settings["folder_path"],
                "target_extensions": st.session_state.settings["target_extensions"],
                "always_include": st.session_state.settings["always_include"],
                "excluded_dirs": st.session_state.settings["excluded_dirs"],
                "system_prompt": st.session_state.settings["system_prompt"],
            }
            self.settings_manager.save_settings(
                new_settings, filename=f"settings/{selected_file}"
            )
            st.sidebar.success(f"Settings saved to {selected_file}!")

            # Offer to download settings file
            settings_json = json.dumps(new_settings, ensure_ascii=False, indent=2)
            st.sidebar.download_button(
                label="Download settings file",
                data=settings_json,
                file_name=selected_file,
                mime="application/json",
            )

        if st.sidebar.button("Load settings"):
            st.session_state["settings"] = self.settings_manager.load_settings(
                filename=f"settings/{selected_file}"
            )
            st.sidebar.success(f"Settings loaded from {selected_file}!")

        settings_file = st.sidebar.file_uploader(
            "Upload settings file",
            type=["json"],
            help="Upload a local JSON settings file",
        )

        if settings_file is not None:
            # Load settings from uploaded file
            st.session_state["settings"] = (
                self.settings_manager.load_settings_from_file(settings_file)
            )
            st.sidebar.success(f"Settings loaded from file {settings_file.name}!")

    def render(self) -> Tuple[str, str, float, int]:
        """
        Renders the settings sidebar and returns the selected strategy, model, temperature, and max tokens.

        Returns
        -------
        Tuple[str, str, float, int]
            A tuple containing the selected strategy, model, temperature, and max tokens.
        """
        st.sidebar.title("Настройки")
        self._handle_settings()

        unique_key = hash(json.dumps(st.session_state["settings"], sort_keys=True))

        # -----------------------------------------------
        st.sidebar.write("---")

        # Display and update settings fields
        st.session_state.settings["folder_path"] = st.sidebar.text_input(
            "Folder path",
            st.session_state.settings.get("folder_path", ""),
            key=f"folder_path_{unique_key}",
            help="Enter the directory path",
        )
        st.session_state.settings["target_extensions"] = st.sidebar.text_input(
            "Target extensions",
            st.session_state.settings.get("target_extensions", ""),
            key=f"target_extensions_{unique_key}",
            help="Enter extensions separated by commas, e.g., .py,.txt,.md",
        )
        st.session_state.settings["always_include"] = st.sidebar.text_input(
            "Always include files",
            st.session_state.settings.get("always_include", ""),
            key=f"always_include_{unique_key}",
            help="Enter file names separated by commas",
        )
        st.session_state.settings["excluded_dirs"] = st.sidebar.text_input(
            "Excluded directories",
            st.session_state.settings.get("excluded_dirs", ""),
            key=f"excluded_dirs_{unique_key}",
            help="Enter directories separated by commas",
        )
        st.session_state.settings["system_prompt"] = st.sidebar.text_area(
            "System prompt",
            st.session_state.settings.get("system_prompt", ""),
            key=f"system_prompt_{unique_key}",
            help="System prompt for LLM",
        )

        # -----------------------------------------------
        st.sidebar.write("---")

        # Select chat model
        chosen_model = st.sidebar.selectbox(
            "Model name",
            (self.models_list),
            help="Select a model from the available options",
        )

        current_strategy, current_model = chosen_model.split(DIVIDER)
        self.output_max_tokens = self.strategies[
            current_strategy
        ].get_output_max_tokens(current_model)

        # Select temperature and max tokens
        temperature = st.sidebar.slider(
            "Temperature",
            0.0,
            1.0,
            0.0,
            help="""
            Parameter that controls the randomness of the model's responses.
            A value of 0 means the model will generate more predictable and consistent text.""",
        )
        max_tokens = st.sidebar.number_input(
            "Max tokens",
            min_value=1000,
            max_value=self.output_max_tokens,
            value=self.output_max_tokens,
            step=100,
            help="""
            The maximum number of tokens that can be generated in the response.
            This helps limit the length of the output.""",
        )

        return current_strategy, current_model, temperature, max_tokens
