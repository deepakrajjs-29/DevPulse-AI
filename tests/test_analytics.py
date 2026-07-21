"""
Unit tests for DevPulse AI Analytics Calculator (Phase 1 & Phase 2 telemetry).
"""

import unittest
from devpulse.analytics.calculator import AnalyticsCalculator
from devpulse.config.manager import PortfolioConfig
from devpulse.domain.models import Repository, UserProfile


class TestAnalyticsCalculator(unittest.TestCase):
    """Test suite verifying mathematical aggregations, language ratios, health, growth, and trends."""

    def setUp(self):
        self.config = PortfolioConfig(
            top_languages_count=3,
            featured_repos_count=2,
            include_forks=False,
        )
        self.calculator = AnalyticsCalculator(config=self.config)

        self.user = UserProfile(
            login="testdev",
            name="Test Developer",
            avatar_url="https://example.com/avatar.png",
            html_url="https://github.com/testdev",
            bio="Open Source Developer",
            company="Tech Corp",
            location="San Francisco, CA",
            blog="https://testdev.io",
            public_repos=3,
            public_gists=1,
            followers=50,
            following=10,
            created_at="2020-01-01T00:00:00Z",
        )

        self.repo1 = Repository(
            id=1,
            name="awesome-python",
            full_name="testdev/awesome-python",
            description="Python utility repo",
            html_url="https://github.com/testdev/awesome-python",
            stargazers_count=100,
            forks_count=20,
            watchers_count=15,
            open_issues_count=2,
            primary_language="Python",
            languages={"Python": 8000, "HTML": 2000},
            license_name="MIT License",
            created_at="2021-05-10T12:00:00Z",
            updated_at="2026-06-01T00:00:00Z",
        )

        self.repo2 = Repository(
            id=2,
            name="js-frontend",
            full_name="testdev/js-frontend",
            description="React frontend application",
            html_url="https://github.com/testdev/js-frontend",
            stargazers_count=50,
            forks_count=10,
            watchers_count=5,
            open_issues_count=1,
            primary_language="TypeScript",
            languages={"TypeScript": 6000, "JavaScript": 4000},
            license_name="Apache-2.0",
            created_at="2022-08-15T12:00:00Z",
            updated_at="2026-07-01T00:00:00Z",
        )

        self.repo_fork = Repository(
            id=3,
            name="forked-repo",
            full_name="testdev/forked-repo",
            description="Forked library",
            html_url="https://github.com/testdev/forked-repo",
            stargazers_count=5,
            forks_count=0,
            watchers_count=1,
            open_issues_count=0,
            primary_language="C++",
            is_fork=True,
            created_at="2023-01-01T00:00:00Z",
        )

    def test_analytics_calculation(self):
        """Verify summary math totals and language percentages across repos."""
        repos = [self.repo1, self.repo2, self.repo_fork]
        analytics = self.calculator.calculate(self.user, repos)

        self.assertEqual(analytics.total_repos, 3)
        self.assertEqual(analytics.total_stars, 155)
        self.assertEqual(analytics.total_forks, 30)

        top_langs = analytics.top_languages
        self.assertEqual(len(top_langs), 3)
        self.assertEqual(top_langs[0].name, "Python")
        self.assertEqual(top_langs[0].percentage, 40.0)

    def test_phase2_health_and_growth_analytics(self):
        """Verify Phase 2 project health, growth, coding trends, and insights math."""
        repos = [self.repo1, self.repo2]
        analytics = self.calculator.calculate(self.user, repos)

        # Health metrics
        self.assertIsNotNone(analytics.project_health)
        self.assertEqual(analytics.project_health.active_repos_count, 2)
        self.assertEqual(analytics.project_health.license_coverage_pct, 100.0)
        self.assertEqual(analytics.project_health.description_coverage_pct, 100.0)

        # Growth metrics
        self.assertIsNotNone(analytics.repository_growth)
        self.assertEqual(analytics.repository_growth.oldest_repo_name, "awesome-python")
        self.assertEqual(analytics.repository_growth.newest_repo_name, "js-frontend")
        self.assertEqual(analytics.repository_growth.avg_stars_per_repo, 75.0)

        # Coding trends
        self.assertIsNotNone(analytics.coding_trend)
        self.assertEqual(analytics.coding_trend.primary_trend_language, "Python")
        self.assertGreaterEqual(analytics.coding_trend.language_diversity_score, 3)

        # Portfolio insights
        self.assertIsNotNone(analytics.portfolio_insights)
        self.assertEqual(analytics.portfolio_insights.strongest_repo_name, "awesome-python")
        self.assertEqual(analytics.portfolio_insights.health_overview_status, "Optimal")


if __name__ == "__main__":
    unittest.main()
