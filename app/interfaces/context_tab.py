"""
Implements the context tab in the Streamlit app, managing context files and displaying context-related information.
"""

import streamlit as st
import pandas as pd

from managers.file_manager import FileManager


class ContextTab:
    def __init__(self, file_manager: FileManager):
        self.settings = st.session_state["settings"]
        self.file_manager = file_manager

    def update_context(self):
        files = self.file_manager.read_files(
            folder_path=self.settings["folder_path"],
            target_extensions=self.settings["target_extensions"],
            always_include=self.settings["always_include"],
            excluded_dirs=self.settings["excluded_dirs"],
        )

        st.session_state["full_context"] = files
        st.session_state["context"] = st.session_state["full_context"]

        if "update_context_key" not in st.session_state:
            st.session_state["update_context_key"] = 0
        else:
            st.session_state["update_context_key"] += 1

    def display_files_info(self):
        st.write(
            "Total files:",
            sum([1 for _ in st.session_state["context"]]),
        )
        st.write(
            "Total tokens:",
            sum([x["tokens"] for x in st.session_state["context"]]),
        )
        st.write(
            "Total lines:",
            sum([x["lines"] for x in st.session_state["context"]]),
        )

    def render(self):
        if st.button("Обновить контекст"):
            self.update_context()

        if "context" in st.session_state:
            update_context_key = (
                st.session_state["update_context_key"]
                if st.session_state["update_context_key"]
                else 0
            )

            st.session_state["files_list"] = st.data_editor(
                pd.DataFrame(
                    [
                        {
                            "Path": item["path"],
                            "Tokens": item["tokens"],
                            "Lines": item["lines"],
                            "Enable": True,
                        }
                        for item in st.session_state["full_context"]
                    ]
                ),
                disabled=["path", "tokens", "lines"],
                key=update_context_key,
            )

            enabled_paths = st.session_state["files_list"][
                st.session_state["files_list"]["Enable"]
            ]["Path"].tolist()

            st.session_state["context"] = [
                item
                for item in st.session_state["full_context"]
                if item["path"] in enabled_paths
            ]

            self.display_files_info()

        with st.expander("System prompt", expanded=False):
            st.text(self.settings["system_prompt"])

        if "context" in st.session_state:
            with st.expander("Files data", expanded=False):
                st.write(st.session_state["context"])
