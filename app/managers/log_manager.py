"""
Manages the logging functionality, allowing the addition and retrieval of log messages with timestamps.
"""

import datetime


class LogManager:
    def __init__(self):
        self.logs = []

    def add_log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"{timestamp} - {message}")

    def get_logs(self):
        return self.logs
