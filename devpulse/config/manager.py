"""
Configuration Manager for DevPulse AI.

Loads, validates, and manages environment variables and YAML settings.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from dotenv import load_dotenv

from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.config")


@dataclass
class AppConfig:
    name: str = "DevPulse AI"
    version: str = "1.0.0"
    description: str = "GitHub Portfolio Assistant"


@dataclass
class GitHubConfig:
    token: Optional[str] = None
    username: str = ""


@dataclass
class PortfolioConfig:
    top_languages_count: int = 6
    featured_repos_count: int = 4
    recent_repos_count: int = 6
    include_forks: bool = False
    include_archived: bool = False
    featured_repo_names: List[str] = field(default_factory=list)


@dataclass
class TemplatesConfig:
    readme_template: str = "templates/default_readme.md.j2"


@dataclass
class OutputConfig:
    directory: str = "output"
    analytics_file: str = "analytics.json"
    readme_file: str = "README.md"
    history_directory: str = "output/history"


@dataclass
class APIConfig:
    timeout: int = 10
    max_workers: int = 5
    min_rate_limit_warning: int = 10


class ConfigManager:
    """Centralized configuration loader supporting environment variables and YAML files."""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        env_file: Optional[Path] = None,
    ):
        self.root_dir = Path.cwd()
        self.config_path = config_path or (self.root_dir / "config" / "config.yaml")
        self.env_file = env_file or (self.root_dir / ".env")

        if self.env_file.exists():
            load_dotenv(dotenv_path=self.env_file)
            logger.debug(f"Loaded environment variables from: {self.env_file}")

        self.app = AppConfig()
        self.github = GitHubConfig()
        self.portfolio = PortfolioConfig()
        self.templates = TemplatesConfig()
        self.output = OutputConfig()
        self.api = APIConfig()

        self._load_env_vars()
        self._load_yaml_config()

    def _load_env_vars(self) -> None:
        """Loads and parses environment configuration."""
        token = os.getenv("GITHUB_TOKEN", "").strip()
        username = os.getenv("GITHUB_USERNAME", "").strip()

        self.github.token = token if token else None
        self.github.username = username

        if not self.github.token:
            logger.warning(
                "GITHUB_TOKEN is not set. Operating in unauthenticated mode "
                "(Rate limit: 60 requests/hour)."
            )
        else:
            logger.info("GitHub authentication token detected.")

    def _load_yaml_config(self) -> None:
        """Loads YAML settings file if present."""
        if not self.config_path.exists():
            logger.warning(
                f"Config file not found at {self.config_path}. Using default settings."
            )
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = yaml.safe_load(f) or {}

            if "app" in data and isinstance(data["app"], dict):
                app_data = data["app"]
                self.app.name = app_data.get("name", self.app.name)
                self.app.version = app_data.get("version", self.app.version)
                self.app.description = app_data.get(
                    "description", self.app.description
                )

            if "portfolio" in data and isinstance(data["portfolio"], dict):
                pf = data["portfolio"]
                self.portfolio.top_languages_count = pf.get(
                    "top_languages_count", self.portfolio.top_languages_count
                )
                self.portfolio.featured_repos_count = pf.get(
                    "featured_repos_count", self.portfolio.featured_repos_count
                )
                self.portfolio.recent_repos_count = pf.get(
                    "recent_repos_count", self.portfolio.recent_repos_count
                )
                self.portfolio.include_forks = pf.get(
                    "include_forks", self.portfolio.include_forks
                )
                self.portfolio.include_archived = pf.get(
                    "include_archived", self.portfolio.include_archived
                )
                self.portfolio.featured_repo_names = pf.get(
                    "featured_repo_names", self.portfolio.featured_repo_names
                )

            if "templates" in data and isinstance(data["templates"], dict):
                tmpl = data["templates"]
                self.templates.readme_template = tmpl.get(
                    "readme_template", self.templates.readme_template
                )

            if "output" in data and isinstance(data["output"], dict):
                out = data["output"]
                self.output.directory = out.get("directory", self.output.directory)
                self.output.analytics_file = out.get(
                    "analytics_file", self.output.analytics_file
                )
                self.output.readme_file = out.get(
                    "readme_file", self.output.readme_file
                )
                self.output.history_directory = out.get(
                    "history_directory", self.output.history_directory
                )

            if "api" in data and isinstance(data["api"], dict):
                api = data["api"]
                self.api.timeout = api.get("timeout", self.api.timeout)
                self.api.max_workers = api.get("max_workers", self.api.max_workers)
                self.api.min_rate_limit_warning = api.get(
                    "min_rate_limit_warning", self.api.min_rate_limit_warning
                )

            logger.debug(f"Loaded YAML configuration from: {self.config_path}")

        except Exception as e:
            logger.error(f"Error parsing YAML configuration file ({self.config_path}): {e}")

    def set_username(self, username: str) -> None:
        """Sets or overrides target GitHub username."""
        self.github.username = username.strip()

    def get_output_directory(self) -> Path:
        """Returns target output Path instance."""
        return self.root_dir / self.output.directory

    def get_history_directory(self) -> Path:
        """Returns target historical snapshot directory Path instance."""
        return self.root_dir / self.output.history_directory

    def get_analytics_path(self) -> Path:
        """Returns absolute path for target analytics JSON export."""
        return self.get_output_directory() / self.output.analytics_file

    def get_readme_path(self) -> Path:
        """Returns absolute path for target Markdown README export."""
        return self.get_output_directory() / self.output.readme_file
