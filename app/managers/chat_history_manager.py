"""
Manages the saving of chat histories.
"""

from typing import List, Dict
import os
from datetime import datetime


class ChatHistoryManager:
    def __init__(self, directory: str = "chat_histories"):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_chat_history(
        self, messages: List[Dict[str, str]], filename: str = None
    ) -> str:
        if filename is None:
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".md"
        filepath = os.path.join(self.directory, filename)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(self._convert_messages_to_md(messages))
        return filepath

    def _convert_messages_to_md(self, messages: List[Dict[str, str]]) -> str:
        md_content = (
            f"# Chat History {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}\n\n"
        )
        for message in messages:
            md_content += f"**Role:** {message['role']}\n"
            md_content += message["content"]
            md_content += "  \n\n---\n\n"

        return md_content
