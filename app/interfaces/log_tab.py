import streamlit as st


class LogTab:
    def __init__(self, log_manager):
        self.log_manager = log_manager

    def render(self):
        if "logs" not in st.session_state:
            st.session_state["logs"] = []

        if len(self.log_manager.get_logs()) > 0:
            st.session_state["logs"].append(self.log_manager.get_logs())

        if len(st.session_state["logs"]) > 0:
            for item_log in st.session_state["logs"]:
                with st.expander("Лог системы", expanded=True):
                    st.text("\n".join(item_log))
