"""Provide a uniform logger for workflows."""
import logging
import os


def get_logger(name: str, log_level=os.getenv('LOG_LEVEL', 'WARN')) -> logging.Logger:
    """
    Get a logger.

    The log level can be set by setting the LOG_LEVEL environment variable.

    Parameters
    ----------
    name : str
        The name of the logger to be returned.
    log_level : _type_, optional
        The log level, by default "WARN".

    Returns
    -------
    logging.Logger
        A logger suitable for using in the workflows.
    """
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
