"""
Implements the log tab in the Streamlit app, displaying logs and total costs.
"""

import streamlit as st

from managers.log_manager import LogManager


class LogTab:
    """Class representing the log tab in the Streamlit app.

    Parameters
    ----------
    log_manager : LogManager
        Instance of the LogManager class for managing logs.

    Methods
    -------
    render()
        Renders the log tab in the Streamlit app.
    """

    def __init__(self, log_manager: LogManager):
        self.log_manager = log_manager

    def render(self) -> None:
        """
        Renders the log tab in the Streamlit app.
        """
        if "total_cost" in st.session_state:
            st.write(
                f" Total cost: {st.session_state['total_cost']} $ (~{st.session_state['total_cost']*100:.2f} Rub)",
            )

        if "logs" not in st.session_state:
            st.session_state["logs"] = []

        if len(self.log_manager.get_logs()) > 0:
            st.session_state["logs"].append(self.log_manager.get_logs())

        if len(st.session_state["logs"]) > 0:
            for item_log in st.session_state["logs"]:
                with st.expander(item_log[0], expanded=True):
                    st.text("\n".join(item_log))
