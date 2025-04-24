# Functions for logging to console


import sys
import datetime


def get_timestamp() -> str:
    """Get the current timestamp for alerting purposes

    Returns:
            str: The current timestamp
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def __log(mac: str, message: str, file):
    """Log a message to the given FD

    Args:
        mac (str): corresponding MAC address
        message (str): Message
        file (_type_): stdout/err
    """
    print(f"[{get_timestamp()}] [{mac}] {message}", file=file)


def log(mac: str, message: str):
    """Log a normal message

    Args:
        mac (str): data
        message (str): data
    """
    __log(mac, message, sys.stdout)


def err(mac: str, message: str):
    """Log an error

    Args:
        mac (str): data
        message (str): data
    """
    __log(mac, message, sys.stderr)
