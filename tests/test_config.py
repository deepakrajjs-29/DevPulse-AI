"""
Unit tests for DevPulse AI Configuration Manager.
"""

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from devpulse.config.manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test suite verifying environment variable loading and YAML parsing."""

    def test_default_config_initialization(self):
        """Verify default configuration attributes are instantiated cleanly."""
        config_mgr = ConfigManager()
        self.assertEqual(config_mgr.app.name, "DevPulse AI")
        self.assertEqual(config_mgr.portfolio.top_languages_count, 6)
        self.assertEqual(config_mgr.output.directory, "output")

    def test_username_override(self):
        """Verify setting username updates github configuration."""
        config_mgr = ConfigManager()
        config_mgr.set_username("testuser")
        self.assertEqual(config_mgr.github.username, "testuser")

    def test_path_resolvers(self):
        """Verify path helper functions return absolute Path objects."""
        config_mgr = ConfigManager()
        out_dir = config_mgr.get_output_directory()
        analytics_path = config_mgr.get_analytics_path()
        readme_path = config_mgr.get_readme_path()

        self.assertIsInstance(out_dir, Path)
        self.assertTrue(str(analytics_path).endswith("analytics.json"))
        self.assertTrue(str(readme_path).endswith("README.md"))

    def test_custom_yaml_loading(self):
        """Verify loading settings from custom YAML file."""
        with TemporaryDirectory() as tmp_dir:
            yaml_path = Path(tmp_dir) / "custom_config.yaml"
            yaml_path.write_text(
                """
app:
  name: "Custom DevPulse"
portfolio:
  top_languages_count: 10
  featured_repos_count: 5
""",
                encoding="utf-8",
            )
            config_mgr = ConfigManager(config_path=yaml_path)
            self.assertEqual(config_mgr.app.name, "Custom DevPulse")
            self.assertEqual(config_mgr.portfolio.top_languages_count, 10)
            self.assertEqual(config_mgr.portfolio.featured_repos_count, 5)


if __name__ == "__main__":
    unittest.main()
