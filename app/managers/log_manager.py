"""
Manages the logging functionality, allowing the addition and retrieval of log messages with timestamps.
"""

import os
from typing import List
import datetime


class LogManager:
    """
    Class for managing logging.

    Attributes
    ----------
    logs : List[str]
        List of log messages.
    log_file_path : str
        Path to the log file.

    Methods
    -------
    add_log(message: str) -> None:
        Adds a log message with a timestamp.
    get_logs() -> List[str]:
        Returns a list of log messages.
    """

    def __init__(self, log_file_path: str = "logs/app.log"):
        self.logs = []
        self.log_file_path = log_file_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    def add_log(self, message: str) -> None:
        """
        Adds a log message with a timestamp.

        Parameters
        ----------
        message : str
            Log message.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {message}"
        self.logs.append(log_entry)

        # Write the log entry to the file
        with open(self.log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry + "\n")

    def get_logs(self) -> List[str]:
        """
        Returns a list of log messages.

        Returns
        -------
        List[str]
            List of log messages.
        """
        return self.logs
