"""
Unit tests for DevPulse AI GitHub API Client.
"""

import unittest
from unittest.mock import MagicMock, patch
import requests

from devpulse.api.client import GitHubClient
from devpulse.api.exceptions import (
    AuthenticationError,
    RateLimitExceededError,
    ResourceNotFoundError,
)


class TestGitHubClient(unittest.TestCase):
    """Test suite verifying GitHub API client network logic, error handling, and model mappings."""

    def setUp(self):
        self.client = GitHubClient(token="mock_token", timeout=5, max_workers=2)

    @patch.object(requests.Session, "get")
    def test_get_user_profile_success(self, mock_get):
        """Verify successful user profile fetching and domain object mapping."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {
            "login": "octocat",
            "name": "The Octocat",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "html_url": "https://github.com/octocat",
            "bio": "GitHub Mascot",
            "public_repos": 8,
            "followers": 1000,
            "following": 5,
            "created_at": "2011-01-25T18:44:36Z",
        }
        mock_get.return_value = mock_response

        profile = self.client.get_user_profile("octocat")
        self.assertEqual(profile.login, "octocat")
        self.assertEqual(profile.name, "The Octocat")
        self.assertEqual(profile.public_repos, 8)
        self.assertEqual(profile.followers, 1000)

    @patch.object(requests.Session, "get")
    def test_authentication_error_401(self, mock_get):
        """Verify HTTP 401 raises AuthenticationError."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.headers = {}
        mock_get.return_value = mock_response

        with self.assertRaises(AuthenticationError):
            self.client.get_user_profile("invalid_token_user")

    @patch.object(requests.Session, "get")
    def test_resource_not_found_404(self, mock_get):
        """Verify HTTP 404 raises ResourceNotFoundError."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {}
        mock_get.return_value = mock_response

        with self.assertRaises(ResourceNotFoundError):
            self.client.get_user_profile("non_existent_user_99999")

    @patch.object(requests.Session, "get")
    def test_rate_limit_exceeded_403(self, mock_get):
        """Verify HTTP 403 with 0 remaining rate limit raises RateLimitExceededError."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.headers = {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1600000000"}
        mock_get.return_value = mock_response

        with self.assertRaises(RateLimitExceededError):
            self.client.get_user_profile("throttled_user")


if __name__ == "__main__":
    unittest.main()
