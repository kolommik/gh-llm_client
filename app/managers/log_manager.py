"""
Manages the logging functionality, allowing the addition and retrieval of log messages with timestamps.
"""

from typing import List
import datetime


class LogManager:
    """
    Class for managing logging.

    Attributes
    ----------
    logs : List[str]
        List of log messages.

    Methods
    -------
    add_log(message: str) -> None:
        Adds a log message with a timestamp.
    get_logs() -> List[str]:
        Returns a list of log messages.
    """

    def __init__(self):
        self.logs = []

    def add_log(self, message: str) -> None:
        """
        Adds a log message with a timestamp.

        Parameters
        ----------
        message : str
            Log message.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"{timestamp} - {message}")

    def get_logs(self) -> List[str]:
        """
        Returns a list of log messages.

        Returns
        -------
        List[str]
            List of log messages.
        """
        return self.logs
