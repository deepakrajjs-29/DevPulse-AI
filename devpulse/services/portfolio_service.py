"""
Portfolio Service Orchestrator for DevPulse AI.

High-level application coordinator executing the end-to-end telemetry pipeline:
1. Validates configuration and targets.
2. Authenticates and fetches GitHub developer profile & repositories.
3. Computes analytics metrics, health, growth, coding trends, and insights.
4. Loads previous historical snapshot and calculates real growth deltas.
5. Exports structured JSON analytics, dynamic README markdown, and daily historical snapshot.
6. Performs SHA-256 change detection scan across output artifacts.
"""

from pathlib import Path
from typing import List, Optional, Tuple

from devpulse.analytics.calculator import AnalyticsCalculator
from devpulse.analytics.history import HistoryManager
from devpulse.api.client import GitHubClient
from devpulse.api.exceptions import ConfigurationError
from devpulse.automation.change_detector import ChangeDetector
from devpulse.config.manager import ConfigManager
from devpulse.domain.models import PortfolioAnalytics
from devpulse.exporters.json_exporter import JSONExporter
from devpulse.exporters.markdown_exporter import MarkdownExporter
from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.service")


class PortfolioService:
    """Orchestrates end-to-end portfolio analysis, historical tracking, artifact generation, and change detection."""

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """Initializes the PortfolioService pipeline.

        Args:
            config_manager: Optional ConfigManager instance.
        """
        self.config_manager = config_manager or ConfigManager()
        self.change_detector = ChangeDetector()
        self.history_manager = HistoryManager()

    def run(
        self, username_override: Optional[str] = None, check_changes_only: bool = False
    ) -> Tuple[PortfolioAnalytics, List[Path]]:
        """Executes the portfolio assistant engine pipeline.

        Args:
            username_override: Optional username string passed via CLI args.
            check_changes_only: If True, calculates changes without overwriting if unchanged.

        Returns:
            Tuple[PortfolioAnalytics, List[Path]]: Analytics object and list of changed file paths.

        Raises:
            ConfigurationError: If no username is provided in environment or CLI.
        """
        if username_override:
            self.config_manager.set_username(username_override)

        username = self.config_manager.github.username
        if not username:
            logger.error("No GitHub username specified. Set GITHUB_USERNAME in .env or pass via CLI.")
            raise ConfigurationError(
                "Missing GitHub username. Please set GITHUB_USERNAME or use --username flag."
            )

        logger.info(f"Starting DevPulse AI portfolio pipeline for user: '{username}'")

        # 1. Initialize API Client
        client = GitHubClient(
            token=self.config_manager.github.token,
            timeout=self.config_manager.api.timeout,
            max_workers=self.config_manager.api.max_workers,
            min_rate_limit_warning=self.config_manager.api.min_rate_limit_warning,
        )

        # 2. Fetch User Profile and Repositories
        user_profile = client.get_user_profile(username)
        repositories = client.get_repositories(username)

        # 3. Calculate Core & Phase 2 Analytics
        calculator = AnalyticsCalculator(config=self.config_manager.portfolio)
        analytics = calculator.calculate(user=user_profile, repositories=repositories)

        # 4. Process Historical Snapshots & Deltas
        history_dir = self.config_manager.get_history_directory()
        prev_snapshot = self.history_manager.load_previous_snapshot(history_dir)
        delta = self.history_manager.calculate_delta(analytics, prev_snapshot)
        analytics.portfolio_delta = delta

        # 5. Ensure Output Directories
        output_dir = self.config_manager.get_output_directory()
        output_dir.mkdir(parents=True, exist_ok=True)

        json_path = self.config_manager.get_analytics_path()
        readme_path = self.config_manager.get_readme_path()
        template_path = self.config_manager.root_dir / self.config_manager.templates.readme_template

        # 6. Export Latest JSON & Markdown Artifacts
        json_exporter = JSONExporter()
        json_exporter.export(analytics, json_path)

        markdown_exporter = MarkdownExporter(template_path=template_path)
        markdown_exporter.export(analytics, readme_path)

        # 7. Save Daily Historical Snapshot (output/history/YYYY-MM-DD.json)
        app_version = self.config_manager.app.version
        snapshot_path = self.history_manager.save_snapshot(
            analytics=analytics,
            history_dir=history_dir,
            app_version=app_version,
        )

        # 8. Perform SHA-256 Change Detection Scan Across Generated Artifacts
        changed_paths = self.change_detector.detect_changes({
            json_path: json_path.read_text(encoding="utf-8"),
            readme_path: readme_path.read_text(encoding="utf-8"),
            snapshot_path: snapshot_path.read_text(encoding="utf-8"),
        })

        logger.info(
            f"DevPulse AI Pipeline completed successfully! Artifacts saved in '{output_dir}'. "
            f"({len(changed_paths)} files changed)"
        )
        return analytics, changed_paths
