"""
Implements the context tab in the Streamlit app, managing context files and displaying context-related information.
"""

import streamlit as st


class ContextTab:
    def __init__(self, settings, file_manager):
        self.settings = settings
        self.file_manager = file_manager

    def render(self):
        if st.button("Обновить контекст"):
            files = self.file_manager.read_files(
                folder_path=self.settings["folder_path"],
                target_extensions=self.settings["target_extensions"],
                always_include=self.settings["always_include"],
                excluded_dirs=self.settings["excluded_dirs"],
            )

            st.session_state["context"] = files

        if "context" in st.session_state:
            st.write(
                "Total tokens:",
                sum([x["tokens"] for x in st.session_state["context"]]),
            )
            st.write(
                "Total lines:",
                sum([x["lines"] for x in st.session_state["context"]]),
            )
            st.table(
                [
                    {
                        "path": item["path"],
                        "tokens": item["tokens"],
                        "length (symbols)": item["length"],
                        "lines": item["lines"],
                    }
                    for item in st.session_state["context"]
                ]
            )

        with st.expander("System prompt", expanded=False):
            st.text(self.settings["system_prompt"])

        if "context" in st.session_state:
            with st.expander("Files data", expanded=False):
                st.write(st.session_state["context"])
