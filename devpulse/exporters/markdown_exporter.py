"""
Markdown README Exporter for DevPulse AI.

Uses Jinja2 template engine with custom formatting filters (k-format, progress bar,
markdown table cell sanitizer, date formatting) to render dynamic README files.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from jinja2 import Environment, FileSystemLoader

from devpulse.domain.models import PortfolioAnalytics
from devpulse.exporters.base import BaseExporter
from devpulse.utils.file_io import write_file
from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.exporters.markdown")


def filter_k_format(value: Any) -> str:
    """Jinja filter to format numbers into clean k notation (e.g. 1500 -> 1.5k)."""
    try:
        num = float(value)
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M".replace(".0M", "M")
        if num >= 1_000:
            return f"{num / 1_000:.1f}k".replace(".0k", "k")
        return str(int(num))
    except (ValueError, TypeError):
        return str(value)


def filter_percentage_bar(percentage: float, length: int = 10) -> str:
    """Jinja filter to render a visual ASCII percentage bar (e.g. ██████░░░░)."""
    try:
        pct = max(0.0, min(100.0, float(percentage)))
        filled = int(round((pct / 100.0) * length))
        empty = length - filled
        return "█" * filled + "░" * empty
    except (ValueError, TypeError):
        return "░" * length


def filter_sanitize_markdown(text: Optional[str]) -> str:
    """Jinja filter to sanitize raw repository descriptions for markdown table rendering."""
    if not text:
        return "No description provided."
    clean = text.replace("|", "\\|").replace("\n", " ").replace("\r", "")
    return clean.strip()


def filter_format_date(date_str: Optional[str]) -> str:
    """Jinja filter to format ISO timestamp strings into clean human dates."""
    if not date_str:
        return "N/A"
    try:
        clean_str = date_str.split(".")[0].replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_str)
        return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str[:10] if len(date_str) >= 10 else date_str


class MarkdownExporter(BaseExporter):
    """Exports portfolio analytics into a dynamic README markdown file using Jinja2 templates."""

    def __init__(self, template_path: Path):
        """Initializes MarkdownExporter.

        Args:
            template_path: Path object pointing to the target .j2 template file.
        """
        self.template_path = Path(template_path).resolve()
        if not self.template_path.is_file():
            raise FileNotFoundError(f"Jinja2 template file not found at: '{self.template_path}'")

        template_dir = self.template_path.parent
        template_name = self.template_path.name

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["k_format"] = filter_k_format
        self.env.filters["percentage_bar"] = filter_percentage_bar
        self.env.filters["sanitize_markdown"] = filter_sanitize_markdown
        self.env.filters["format_date"] = filter_format_date

        self.template = self.env.get_template(template_name)
        logger.debug(f"Initialized MarkdownExporter with template: '{self.template_path}'")

    def export(self, analytics: PortfolioAnalytics, output_path: Path) -> Path:
        """Renders Jinja2 template with analytics context and writes target README file.

        Args:
            analytics: Populated PortfolioAnalytics entity.
            output_path: Destination file Path object.

        Returns:
            Path: Path to written README artifact.
        """
        logger.info(f"Rendering portfolio README template to: '{output_path}'")

        # Context dictionary passed into Jinja2 template
        context = {
            "user": analytics.user,
            "analytics": analytics,
            "summary": {
                "total_repos": analytics.total_repos,
                "total_stars": analytics.total_stars,
                "total_forks": analytics.total_forks,
                "total_watchers": analytics.total_watchers,
                "total_open_issues": analytics.total_open_issues,
            },
            "top_languages": analytics.top_languages,
            "featured_repos": analytics.featured_repos,
            "recent_repos": analytics.recent_repos,
            "project_health": analytics.project_health,
            "repository_growth": analytics.repository_growth,
            "coding_trend": analytics.coding_trend,
            "developer_activity": analytics.developer_activity,
            "portfolio_insights": analytics.portfolio_insights,
            "portfolio_delta": analytics.portfolio_delta,
            "metadata": analytics.metadata,
            "generated_at": analytics.generated_at,
        }

        rendered_markdown = self.template.render(context)
        written_path = write_file(output_path, rendered_markdown)

        logger.info(f"Successfully rendered dynamic README at '{written_path}'")
        return written_path
