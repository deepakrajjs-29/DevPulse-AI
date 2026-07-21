"""
GitHub API client package for DevPulse AI.
"""

from devpulse.api.exceptions import (
    DevPulseException,
    GitHubAPIError,
    AuthenticationError,
    RateLimitExceededError,
    ResourceNotFoundError,
    ConfigurationError,
)
from devpulse.api.client import GitHubClient

__all__ = [
    "DevPulseException",
    "GitHubAPIError",
    "AuthenticationError",
    "RateLimitExceededError",
    "ResourceNotFoundError",
    "ConfigurationError",
    "GitHubClient",
]
