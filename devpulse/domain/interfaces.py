"""
Domain Protocols and Interfaces for DevPulse AI.

Defines abstract contracts for API clients and file exporters to enforce
Dependency Inversion Principle across layers.
"""

from pathlib import Path
from typing import List, Protocol, runtime_checkable

from devpulse.domain.models import PortfolioAnalytics, Repository, UserProfile


@runtime_checkable
class APIClientProtocol(Protocol):
    """Protocol contract for GitHub API Client implementations."""

    def get_user_profile(self, username: str) -> UserProfile:
        """Fetches developer profile telemetry for a given username."""
        ...

    def get_repositories(self, username: str) -> List[Repository]:
        """Fetches all repository entities for a given username."""
        ...


@runtime_checkable
class ExporterProtocol(Protocol):
    """Protocol contract for output exporters (Markdown, JSON, HTML, etc.)."""

    def export(self, analytics: PortfolioAnalytics, output_path: Path) -> Path:
        """Exports portfolio analytics telemetry to a target file path."""
        ...
