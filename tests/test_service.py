"""
Unit tests for DevPulse AI Portfolio Service Pipeline.
"""

import unittest
from unittest.mock import MagicMock, patch
from tempfile import TemporaryDirectory
from pathlib import Path

from devpulse.config.manager import ConfigManager
from devpulse.domain.models import Repository, UserProfile
from devpulse.services.portfolio_service import PortfolioService


class TestPortfolioService(unittest.TestCase):
    """Test suite verifying end-to-end service orchestration."""

    @patch("devpulse.services.portfolio_service.GitHubClient")
    def test_pipeline_execution(self, mock_client_cls):
        """Verify pipeline executes API calls, calculations, exports, and change detection without error."""
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            template_path = tmp_path / "template.j2"
            template_path.write_text("# Portfolio for {{ user.login }}", encoding="utf-8")

            # Mock ConfigManager
            config_mgr = ConfigManager()
            config_mgr.github.username = "testuser"
            config_mgr.output.directory = str(tmp_path / "output")
            config_mgr.templates.readme_template = str(template_path)
            config_mgr.root_dir = tmp_path

            # Mock API Client instance
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.get_user_profile.return_value = UserProfile(
                login="testuser",
                name="Test User",
                avatar_url="",
                html_url="https://github.com/testuser",
                bio="",
                company="",
                location="",
                blog="",
                public_repos=1,
                public_gists=0,
                followers=10,
                following=5,
                created_at="2022-01-01T00:00:00Z",
            )
            mock_client.get_repositories.return_value = [
                Repository(
                    id=1,
                    name="repo1",
                    full_name="testuser/repo1",
                    description="test repo",
                    html_url="https://github.com/testuser/repo1",
                    stargazers_count=10,
                    forks_count=2,
                    watchers_count=1,
                    open_issues_count=0,
                    primary_language="Python",
                )
            ]

            service = PortfolioService(config_manager=config_mgr)
            analytics, changed_files = service.run()

            self.assertEqual(analytics.user.login, "testuser")
            self.assertEqual(analytics.total_stars, 10)
            self.assertTrue(config_mgr.get_analytics_path().is_file())
            self.assertTrue(config_mgr.get_readme_path().is_file())
            self.assertIsInstance(changed_files, list)


if __name__ == "__main__":
    unittest.main()
