"""
Centralized logging utility for DevPulse AI.

Provides structured logging to both console and log files with configurable
verbosity levels and safe formatting.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


# Global logger cache to maintain singletons per logger name
_LOGGERS: dict[str, logging.Logger] = {}


def setup_logger(
    name: str = "devpulse",
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    max_bytes: int = 5_000_000,
    backup_count: int = 3,
) -> logging.Logger:
    """Configures and returns a structured logger with console and file output.

    Args:
        name: The name of the logger namespace.
        log_level: Desired log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to a file where logs should be appended.
        max_bytes: Maximum size of log file before rotation.
        backup_count: Number of rotated log files to retain.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Avoid duplicate handlers if setup is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Log format standard
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Stream (Console) Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    _LOGGERS[name] = logger
    return logger


def get_logger(name: str = "devpulse") -> logging.Logger:
    """Retrieves an existing logger or initializes a default instance.

    Args:
        name: The name of the logger namespace.

    Returns:
        logging.Logger: Logger instance.
    """
    if name in _LOGGERS:
        return _LOGGERS[name]
    return setup_logger(name=name)
