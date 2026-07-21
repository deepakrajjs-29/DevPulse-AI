"""
Custom Exceptions domain for DevPulse AI.

Provides structured domain exception taxonomy for API errors, authentication,
rate limits, missing resources, and configuration errors.
"""

from typing import Optional


class DevPulseException(Exception):
    """Base exception for all DevPulse AI application errors."""

    pass


class ConfigurationError(DevPulseException):
    """Raised when environment or YAML configuration is missing or invalid."""

    pass


class GitHubAPIError(DevPulseException):
    """Raised when a GitHub REST API request fails or returns an HTTP error status."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(GitHubAPIError):
    """Raised when authentication with the GitHub REST API fails (HTTP 401)."""

    def __init__(self, message: str = "Invalid or expired GitHub PAT token."):
        super().__init__(message, status_code=401)


class RateLimitExceededError(GitHubAPIError):
    """Raised when the GitHub API rate limit quota is exhausted (HTTP 403 / 429)."""

    def __init__(self, message: str = "GitHub API rate limit exceeded.", reset_time: Optional[int] = None):
        super().__init__(message, status_code=429)
        self.reset_time = reset_time


class ResourceNotFoundError(GitHubAPIError):
    """Raised when a requested user or repository is not found (HTTP 404)."""

    def __init__(self, resource: str):
        super().__init__(f"Requested GitHub resource not found: '{resource}'", status_code=404)
        self.resource = resource
