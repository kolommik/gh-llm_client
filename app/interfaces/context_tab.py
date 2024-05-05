import streamlit as st

from managers.file_manager import FileManager


class ContextTab:
    def __init__(self, settings):
        self.settings = settings

    def render(self):
        if st.button("Обновить контекст"):
            file_manager = FileManager(
                folder_path=self.settings["folder_path"],
                target_extensions=self.settings["target_extensions"],
                always_include=self.settings["always_include"],
                excluded_dirs=self.settings["excluded_dirs"],
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
                        "length (symbols)": item["length"],
                    }
                    for item in st.session_state["context"]
                ]
            )

        with st.expander("System prompt", expanded=False):
            st.text(self.settings["system_prompt"])

        if "context" in st.session_state:
            with st.expander("Files data", expanded=False):
                st.write(st.session_state["context"])
