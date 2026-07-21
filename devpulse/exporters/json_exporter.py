"""
JSON Analytics Exporter for DevPulse AI.

Serializes PortfolioAnalytics domain models into structured, human-readable JSON payloads.
"""

import json
from pathlib import Path

from devpulse.domain.models import PortfolioAnalytics
from devpulse.exporters.base import BaseExporter
from devpulse.utils.file_io import write_file
from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.exporters.json")


class JSONExporter(BaseExporter):
    """Exports portfolio analytics into a structured JSON file."""

    def __init__(self, indent: int = 2):
        """Initializes JSONExporter.

        Args:
            indent: Formatting indentation spaces (defaults to 2).
        """
        self.indent = indent

    def export(self, analytics: PortfolioAnalytics, output_path: Path) -> Path:
        """Serializes and writes analytics payload to target JSON file.

        Args:
            analytics: Populated PortfolioAnalytics entity.
            output_path: Destination file Path object.

        Returns:
            Path: Path to written JSON artifact.
        """
        logger.info(f"Exporting analytics payload to JSON file: '{output_path}'")
        data_dict = analytics.to_dict()
        json_content = json.dumps(data_dict, indent=self.indent, ensure_ascii=False)

        written_path = write_file(output_path, json_content)
        logger.info(f"Successfully generated JSON analytics artifact at '{written_path}'")
        return written_path
