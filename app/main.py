"""
Main entry point for the Streamlit application.
Initializes the necessary managers and runs the StreamlitInterface.
"""

import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from interfaces.settings_sidebar import SettingsSidebar
from interfaces.log_tab import LogTab
from interfaces.context_tab import ContextTab
from interfaces.chat_tab import ChatTab
from managers.log_manager import LogManager
from managers.file_manager import FileManager
from managers.settings_manager import SettingsManager
from managers.chat_history_manager import ChatHistoryManager
from chat_strategies.openai_strategy import OpenAIChatStrategy
from chat_strategies.anthropic_strategy import AnthropicChatStrategy
from chat_strategies.gemini_strategy import GeminiChatStrategy


class StreamlitInterface:
    """
    Class representing the Streamlit interface for the chat application.

    Parameters
    ----------
    settings_manager : SettingsManager
        Instance of the SettingsManager class for managing application settings.
    log_manager : LogManager
        Instance of the LogManager class for managing logs.
    file_manager : FileManager
        Instance of the FileManager class for managing files.
    chat_history_manager : ChatHistoryManager
        Instance of the ChatHistoryManager class for managing chat history.
    openai_api_key : str, optional
        OpenAI API key. Default is None.
    anthropic_api_key : str, optional
        Anthropic API key. Default is None.

    Methods
    -------
    run()
        Runs the Streamlit interface.
    """

    def __init__(
        self,
        settings_manager: SettingsManager,
        log_manager: LogManager,
        file_manager: FileManager,
        chat_history_manager: ChatHistoryManager,
        openai_api_key: str = None,
        anthropic_api_key: str = None,
        google_api_key: str = None,
    ):
        self.settings_manager = settings_manager
        self.log_manager = log_manager
        self.chat_history_manager = chat_history_manager
        self.file_manager = file_manager

        # TODO - handle error if model list is empty due to missing env keys
        self.strategies = {
            "OpenAI": (
                OpenAIChatStrategy(api_key=openai_api_key) if openai_api_key else None
            ),
            "Anthropic": (
                AnthropicChatStrategy(api_key=anthropic_api_key)
                if anthropic_api_key
                else None
            ),
            "Gemini": (
                GeminiChatStrategy(api_key=google_api_key) if google_api_key else None
            ),
        }

    def run(self):
        """
        Runs the Streamlit interface.
        """
        st.set_page_config(page_title="Chat App", layout="wide")

        # Settings sidebar ==========================================
        self.current_strategy, self.current_model, temperature, max_tokens = (
            SettingsSidebar(self.settings_manager, self.strategies).render()
        )

        # Main interface ============================================
        tab1, tab2, tab3 = st.tabs(["📚 Context", "💬 Chat", "📜 Log"])

        with tab1:
            ContextTab(self.file_manager).render()

        # Chat =======================================================
        with tab2:
            ChatTab(
                self.strategies,
                self.current_strategy,
                self.current_model,
                temperature,
                max_tokens,
                self.log_manager,
                self.chat_history_manager,
            ).render()

        with tab3:
            LogTab(self.log_manager).render()


if __name__ == "__main__":
    load_dotenv(find_dotenv())  # read local.env file
    openai_api_key = os.environ.get("OPENAI_API_KEY", None)
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None)
    google_api_key = os.environ.get("GOOGLE_API_KEY", None)

    settings_manager = SettingsManager()
    log_manager = LogManager()
    chat_history_manager = ChatHistoryManager()
    file_manager = FileManager()

    app = StreamlitInterface(
        settings_manager,
        log_manager,
        file_manager,
        chat_history_manager,
        openai_api_key,
        anthropic_api_key,
        google_api_key,
    )
    app.run()
