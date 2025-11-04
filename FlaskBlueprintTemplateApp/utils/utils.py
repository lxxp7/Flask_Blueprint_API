"""Utils module containing all frequently used functions."""
from typing import Any

from flask import Response, current_app, jsonify


def return_error(err_message: str, status_code: int = 400) -> Response:
    """
    Return a formatted error response with a message and optional status code.

    Args:
        err_message (str): The description of the error message
        status_code (int): The HTTP error status code (default is 400)

    Returns:
        Response: A Flask Response object containing the error message and status code
    """
    return jsonify(
        {"error": err_message}
    ), status_code


def return_response(data: Any, status_code: int = 200 ) -> Response:
    """
    Return a formatted success response with the provided data and status code.

    Args:
        data (any): The data to return

    Returns:
        Response: A Flask Response object containing the data and HTTP status code
    """
    return jsonify(
        {"data": data}
    ), status_code


def log_info(message: str):
    """
    Log an info message in the current app logs.

    Args:
        message (str): the message to log
    """
    current_app.logger.info(message)


def log_error(message: str):
    """
    Log an error message in the current app logs.

    Args:
        message (str): the message to log
    """
    current_app.logger.error(message)


def log_warning(message: str):
    """
    Log a warning message in the current app logs.

    Args:
        message (str): the message to log
    """
    current_app.logger.warning(message)


def get_setting(key, **kwargs):
    """
    Retrieve a configuration value from the application settings.

    Args:
        key (str): The configuration key to fetch.
        **kwargs: Variables for string formatting if the setting is a template.

    Returns:
        Any: The value associated with the given key, formatted if kwargs provided, or None if not found.
    """
    value = current_app.config.get(key)
    if value and kwargs:
        return value.format(**kwargs)
    return value

