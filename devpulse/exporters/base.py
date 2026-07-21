"""
Abstract Base Exporter for DevPulse AI.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from devpulse.domain.models import PortfolioAnalytics


class BaseExporter(ABC):
    """Abstract Base Class for all portfolio exporters."""

    @abstractmethod
    def export(self, analytics: PortfolioAnalytics, output_path: Path) -> Path:
        """Exports portfolio analytics data to a specified destination file path.

        Args:
            analytics: Populated PortfolioAnalytics telemetry payload.
            output_path: Target output Path object.

        Returns:
            Path: Path to the generated output file.
        """
        pass
