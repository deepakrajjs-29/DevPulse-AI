"""
Unit tests for DevPulse AI HistoryManager & Historical Analytics.
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from devpulse.analytics.calculator import AnalyticsCalculator
from devpulse.analytics.history import HistoryManager
from devpulse.domain.models import Repository, UserProfile


class TestHistoryManager(unittest.TestCase):
    """Test suite verifying historical snapshot storage, same-day overwrites, and growth deltas."""

    def setUp(self):
        self.history_mgr = HistoryManager()
        self.calculator = AnalyticsCalculator()

        self.user = UserProfile(
            login="octocat",
            name="The Octocat",
            avatar_url="https://example.com/avatar.png",
            html_url="https://github.com/octocat",
            bio="Mascot",
            company="GitHub",
            location="San Francisco",
            blog="https://github.blog",
            public_repos=2,
            public_gists=0,
            followers=100,
            following=5,
            created_at="2011-01-25T18:44:36Z",
        )

        self.repo1 = Repository(
            id=1,
            name="Spoon-Knife",
            full_name="octocat/Spoon-Knife",
            description="Demo repo",
            html_url="https://github.com/octocat/Spoon-Knife",
            stargazers_count=100,
            forks_count=20,
            watchers_count=15,
            open_issues_count=0,
            primary_language="HTML",
            languages={"HTML": 5000},
        )

    def test_save_snapshot_and_overwrite(self):
        """Verify snapshot file creation and idempotent same-day overwrite."""
        with TemporaryDirectory() as tmp_dir:
            history_dir = Path(tmp_dir)
            analytics = self.calculator.calculate(self.user, [self.repo1])

            # 1. First Save
            snapshot_path1 = self.history_mgr.save_snapshot(analytics, history_dir)
            self.assertTrue(snapshot_path1.is_file())
            content1 = json.loads(snapshot_path1.read_text(encoding="utf-8"))
            self.assertEqual(content1["user"]["login"], "octocat")
            self.assertEqual(content1["metadata"]["generator_name"], "DevPulse AI")

            # 2. Same-day Overwrite with updated star count
            self.repo1.stargazers_count = 150
            analytics2 = self.calculator.calculate(self.user, [self.repo1])
            snapshot_path2 = self.history_mgr.save_snapshot(analytics2, history_dir)

            self.assertEqual(snapshot_path1, snapshot_path2)
            content2 = json.loads(snapshot_path2.read_text(encoding="utf-8"))
            self.assertEqual(content2["summary"]["total_stars"], 150)

    def test_calculate_delta_baseline(self):
        """Verify baseline delta computation when no previous snapshot exists."""
        analytics = self.calculator.calculate(self.user, [self.repo1])
        delta = self.history_mgr.calculate_delta(analytics, previous_snapshot=None)

        self.assertEqual(delta.star_growth, 0)
        self.assertEqual(delta.repo_count_growth, 0)
        self.assertEqual(delta.growth_summary_status, "Baseline Initialized")

    def test_calculate_delta_comparison(self):
        """Verify real delta calculations comparing current state against previous snapshot payload."""
        prev_snapshot = {
            "_snapshot_date": "2026-07-20",
            "summary": {
                "total_repos": 1,
                "total_stars": 80,
                "total_forks": 15,
                "total_watchers": 10,
                "total_open_issues": 0,
            },
            "top_languages": [{"name": "C", "bytes": 1000, "percentage": 100.0}],
            "featured_repositories": [{"name": "Old-Repo"}],
            "recent_repositories": [],
        }

        # Current state has 2 repos, 100 stars (+20), 20 forks (+5), and primary lang HTML
        analytics = self.calculator.calculate(self.user, [self.repo1])
        delta = self.history_mgr.calculate_delta(analytics, prev_snapshot)

        self.assertEqual(delta.star_growth, 20)
        self.assertEqual(delta.fork_growth, 5)
        self.assertEqual(delta.previous_snapshot_date, "2026-07-20")
        self.assertIn("HTML", delta.new_languages)


if __name__ == "__main__":
    unittest.main()
