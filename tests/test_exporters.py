"""
Unit tests for DevPulse AI Exporters (JSONExporter & MarkdownExporter).
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from devpulse.analytics.calculator import AnalyticsCalculator
from devpulse.domain.models import Repository, UserProfile
from devpulse.exporters.json_exporter import JSONExporter
from devpulse.exporters.markdown_exporter import (
    MarkdownExporter,
    filter_k_format,
    filter_percentage_bar,
    filter_sanitize_markdown,
)


class TestExporters(unittest.TestCase):
    """Test suite verifying export formatting, Jinja2 filters, and disk output generation."""

    def setUp(self):
        self.user = UserProfile(
            login="octocat",
            name="Mona Lisa Octocat",
            avatar_url="https://github.com/images/error/octocat_happy.gif",
            html_url="https://github.com/octocat",
            bio="GitHub mascot",
            company="GitHub",
            location="San Francisco",
            blog="https://github.blog",
            public_repos=2,
            public_gists=0,
            followers=5000,
            following=0,
            created_at="2011-01-25T18:44:36Z",
        )
        self.repo = Repository(
            id=1,
            name="Hello-World",
            full_name="octocat/Hello-World",
            description="My first repository on GitHub!",
            html_url="https://github.com/octocat/Hello-World",
            stargazers_count=1500,
            forks_count=250,
            watchers_count=100,
            open_issues_count=0,
            primary_language="C",
            languages={"C": 5000},
            updated_at="2026-05-10T12:00:00Z",
        )
        calculator = AnalyticsCalculator()
        self.analytics = calculator.calculate(self.user, [self.repo])

    def test_custom_jinja_filters(self):
        """Test custom filter functions."""
        self.assertEqual(filter_k_format(1500), "1.5k")
        self.assertEqual(filter_k_format(500), "500")
        self.assertEqual(filter_percentage_bar(50.0, length=10), "█████░░░░░")
        self.assertEqual(filter_sanitize_markdown("Line1|Line2\nLine3"), "Line1\\|Line2 Line3")

    def test_json_exporter(self):
        """Test exporting analytics to JSON file."""
        with TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "analytics.json"
            exporter = JSONExporter()
            written_path = exporter.export(self.analytics, out_file)

            self.assertTrue(written_path.is_file())
            content = json.loads(written_path.read_text(encoding="utf-8"))
            self.assertEqual(content["user"]["login"], "octocat")
            self.assertEqual(content["summary"]["total_stars"], 1500)

    def test_markdown_exporter(self):
        """Test rendering Jinja2 Markdown template."""
        with TemporaryDirectory() as tmp_dir:
            template_file = Path(tmp_dir) / "template.j2"
            template_file.write_text("# Hello {{ user.name }}\nStars: {{ summary.total_stars | k_format }}", encoding="utf-8")

            out_file = Path(tmp_dir) / "README.md"
            exporter = MarkdownExporter(template_path=template_file)
            written_path = exporter.export(self.analytics, out_file)

            self.assertTrue(written_path.is_file())
            content = written_path.read_text(encoding="utf-8")
            self.assertIn("# Hello Mona Lisa Octocat", content)
            self.assertIn("Stars: 1.5k", content)


if __name__ == "__main__":
    unittest.main()
