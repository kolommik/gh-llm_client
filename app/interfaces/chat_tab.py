"""
Implements the chat tab in the Streamlit app, handling user input, displaying chat messages,
and interacting with the selected chat strategy.
"""

from typing import Dict
import streamlit as st
import json
from chat_strategies.chat_model_strategy import ChatModelStrategy
from managers.chat_history_manager import ChatHistoryManager
from managers.log_manager import LogManager


class ChatTab:
    """Class representing the chat tab in the Streamlit app.

    Parameters
    ----------
    strategies : Dict[str, ChatModelStrategy]
        Dictionary mapping strategy names to ChatModelStrategy instances.
    current_strategy : str
        Name of the currently selected chat strategy.
    current_model : str
        Name of the currently selected chat model.
    temperature : float
        Temperature value for the chat model.
    max_tokens : int
        Maximum number of tokens for the chat model.
    log_manager : LogManager
        Instance of the LogManager class for logging.
    chat_history_manager : ChatHistoryManager
        Instance of the ChatHistoryManager class for managing chat history.

    Methods
    -------
    render()
        Renders the chat tab in the Streamlit app.
    """

    def __init__(
        self,
        strategies: Dict[str, ChatModelStrategy],
        current_strategy: str,
        current_model: str,
        temperature: float,
        max_tokens: int,
        log_manager: LogManager,
        chat_history_manager: ChatHistoryManager,
    ):
        self.strategies = strategies
        self.current_strategy = current_strategy
        self.current_model = current_model
        self.settings = st.session_state["settings"]
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.log_manager = log_manager
        self.chat_history_manager = chat_history_manager

    def render(self) -> None:
        """
        Renders the chat tab in the Streamlit app.
        """
        if st.button("Clear chat history"):
            # Clear chat history and logs
            st.session_state["messages"] = []
            st.session_state["logs"] = []
            st.session_state["total_cost"] = 0.0

        if st.button("Save chat"):
            # Save chat history to a file
            filepath = self.chat_history_manager.save_chat_history(
                st.session_state.messages
            )
            st.success(f"Chat saved to file: {filepath}")

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # Display chat messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            if not self.current_strategy:
                st.info("Please add your API key to continue. [OpenAI or Anthropic]")
                st.stop()

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"{prompt}"})
            st.chat_message("user").write(prompt)

            context_str = ""
            if "context" in st.session_state:
                # Build context string from session state
                for item in st.session_state["context"]:
                    context_str += "LOCAL FILEPATH: " + item["path"] + "\n"
                    context_str += "CONTENTS:\n" + item["content"] + "\n\n"

            messages_with_context = []

            if len(context_str) > 0:
                # Add context to messages
                messages_with_context.extend(
                    [
                        {"role": "user", "content": f"Context:\n\n{context_str}"},
                        {"role": "assistant", "content": "Ok, I got it!"},
                    ]
                )

            # Add chat history to messages with context
            messages_with_context.extend(st.session_state.messages.copy())

            # Send message to chat model and get response
            msg = self.strategies[self.current_strategy].send_message(
                system_prompt=self.settings["system_prompt"],
                messages=messages_with_context,
                model_name=self.current_model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            with st.chat_message("assistant"):
                st.write(msg)

            # Get token counts and price from the chat strategy
            input_tokens = self.strategies[self.current_strategy].get_input_tokens()
            output_tokens = self.strategies[self.current_strategy].get_output_tokens()
            total_price = self.strategies[self.current_strategy].get_full_price()

            # Update total cost in session state
            if "total_cost" not in st.session_state:
                st.session_state["total_cost"] = total_price
            else:
                st.session_state["total_cost"] += total_price

            # Display token counts and price
            st.write(
                [
                    f"input_tokens: {input_tokens},output_tokens: {output_tokens}.",
                    f" Price: {total_price} $ (~{total_price*100:.2f} Rub)",
                ]
            )
            # Log chat information
            self.log_manager.add_log(f"{self.current_strategy} - {self.current_model}")
            self.log_manager.add_log(
                f"input_tokens: {input_tokens},output_tokens: {output_tokens}."
            )
            self.log_manager.add_log(
                f" Price: {total_price} $ (~{total_price*100:,.3} Rub)"
            )
            self.log_manager.add_log("=" * 40)
            self.log_manager.add_log(messages_with_context)
            self.log_manager.add_log(
                json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
            )
            self.log_manager.add_log("=" * 40)
            self.log_manager.add_log(msg)
