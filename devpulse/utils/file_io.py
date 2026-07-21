"""
File IO utilities for DevPulse AI.

Provides safe filesystem operations, path resolution, and directory creation.
"""

from pathlib import Path
from typing import Union


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensures that a directory exists, creating missing parent folders if required.

    Args:
        path: Path string or Path object representing the target directory.

    Returns:
        Path: Resolved Path object.
    """
    target_path = Path(path).resolve()
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path


def write_file(path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
    """Writes content to a file, ensuring parent directories exist first.

    Args:
        path: Path string or Path object for the target file.
        content: String content to write.
        encoding: File encoding (defaults to utf-8).

    Returns:
        Path: Path to the written file.
    """
    target_path = Path(path).resolve()
    ensure_directory(target_path.parent)
    target_path.write_text(content, encoding=encoding)
    return target_path


def read_file(path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Reads and returns text content from a file.

    Args:
        path: Path string or Path object for the target file.
        encoding: File encoding (defaults to utf-8).

    Returns:
        str: Content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    target_path = Path(path).resolve()
    if not target_path.is_file():
        raise FileNotFoundError(f"File not found at path: {target_path}")
    return target_path.read_text(encoding=encoding)
