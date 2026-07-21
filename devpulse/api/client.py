"""
GitHub REST API Client for DevPulse AI.

Provides high-performance, resilient access to GitHub user profiles, repositories,
and language statistics with parallel fetching and rate-limit management.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from devpulse.api.exceptions import (
    AuthenticationError,
    GitHubAPIError,
    RateLimitExceededError,
    ResourceNotFoundError,
)
from devpulse.domain.models import Repository, UserProfile
from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.api")


class GitHubClient:
    """Production-grade GitHub REST API client with retry logic and parallel request execution."""

    BASE_URL = "https://api.github.com"

    def __init__(
        self,
        token: Optional[str] = None,
        timeout: int = 10,
        max_workers: int = 5,
        min_rate_limit_warning: int = 10,
    ):
        """Initializes the GitHub API client.

        Args:
            token: Optional GitHub Personal Access Token for authentication.
            timeout: HTTP request timeout in seconds.
            max_workers: Maximum concurrent thread workers for parallel language fetches.
            min_rate_limit_warning: Minimum remaining quota threshold before logging warnings.
        """
        self.token = token
        self.timeout = timeout
        self.max_workers = max_workers
        self.min_rate_limit_warning = min_rate_limit_warning

        # Initialize requests session with connection pooling and retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # Set default headers
        self.session.headers.update(
            {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "DevPulse-AI/1.0.0 (GitHub-Portfolio-Assistant)",
            }
        )
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Executes HTTP GET request against GitHub API with error handling and rate limit checking.

        Args:
            endpoint: API endpoint relative path (e.g. '/users/octocat').
            params: Optional query string parameters.

        Returns:
            Any: Decoded JSON response payload.

        Raises:
            AuthenticationError: On HTTP 401.
            RateLimitExceededError: On HTTP 403 / 429 rate limit errors.
            ResourceNotFoundError: On HTTP 404.
            GitHubAPIError: On unexpected API status codes or network issues.
        """
        url = f"{self.BASE_URL}{endpoint}" if not endpoint.startswith("http") else endpoint
        logger.debug(f"HTTP GET -> {url} (params={params})")

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)

            # Check rate limit headers
            remaining = response.headers.get("X-RateLimit-Remaining")
            reset_time = response.headers.get("X-RateLimit-Reset")

            if remaining is not None:
                rem_val = int(remaining)
                if rem_val <= self.min_rate_limit_warning:
                    logger.warning(
                        f"GitHub API Rate Limit low! Remaining: {rem_val}. Reset epoch: {reset_time}"
                    )

            if response.status_code == 401:
                logger.error("Authentication failed (HTTP 401). Check GITHUB_TOKEN.")
                raise AuthenticationError()

            if response.status_code in (403, 429) and remaining == "0":
                logger.error(f"Rate limit exceeded (HTTP {response.status_code}).")
                reset_epoch = int(reset_time) if reset_time else None
                raise RateLimitExceededError(reset_time=reset_epoch)

            if response.status_code == 404:
                logger.error(f"Resource not found (HTTP 404): {url}")
                raise ResourceNotFoundError(resource=endpoint)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if not isinstance(e, GitHubAPIError):
                logger.error(f"Network error accessing GitHub API: {e}")
                raise GitHubAPIError(f"HTTP Request failed: {e}") from e
            raise

    def get_user_profile(self, username: str) -> UserProfile:
        """Fetches and builds developer UserProfile entity.

        Args:
            username: Target GitHub username.

        Returns:
            UserProfile: Strongly-typed user profile model.
        """
        logger.info(f"Fetching GitHub profile for user: '{username}'")
        data = self._request(f"/users/{username}")

        return UserProfile(
            login=data.get("login", username),
            name=data.get("name"),
            avatar_url=data.get("avatar_url", ""),
            html_url=data.get("html_url", ""),
            bio=data.get("bio"),
            company=data.get("company"),
            location=data.get("location"),
            blog=data.get("blog"),
            public_repos=data.get("public_repos", 0),
            public_gists=data.get("public_gists", 0),
            followers=data.get("followers", 0),
            following=data.get("following", 0),
            created_at=data.get("created_at", ""),
        )

    def _fetch_languages_for_repo(self, repo: Repository) -> Repository:
        """Helper to fetch language breakdown bytes for a single repository."""
        try:
            lang_endpoint = f"/repos/{repo.full_name}/languages"
            lang_data = self._request(lang_endpoint)
            if isinstance(lang_data, dict):
                repo.languages = lang_data
        except Exception as e:
            logger.warning(
                f"Failed to fetch languages for repository '{repo.full_name}': {e}"
            )
        return repo

    def get_repositories(self, username: str) -> List[Repository]:
        """Fetches all repositories for a user with auto-pagination and concurrent language loading.

        Args:
            username: Target GitHub username.

        Returns:
            List[Repository]: List of repository domain entities populated with language stats.
        """
        logger.info(f"Fetching repositories for user: '{username}'")
        repos: List[Repository] = []
        page = 1
        per_page = 100

        while True:
            endpoint = f"/users/{username}/repos"
            params = {"per_page": per_page, "page": page, "sort": "updated"}
            page_data = self._request(endpoint, params=params)

            if not isinstance(page_data, list) or len(page_data) == 0:
                break

            for item in page_data:
                repo = Repository(
                    id=item.get("id", 0),
                    name=item.get("name", ""),
                    full_name=item.get("full_name", ""),
                    description=item.get("description"),
                    html_url=item.get("html_url", ""),
                    stargazers_count=item.get("stargazers_count", 0),
                    forks_count=item.get("forks_count", 0),
                    watchers_count=item.get("watchers_count", 0),
                    open_issues_count=item.get("open_issues_count", 0),
                    primary_language=item.get("language"),
                    topics=item.get("topics", []),
                    license_name=item.get("license", {}).get("name") if item.get("license") else None,
                    created_at=item.get("created_at", ""),
                    updated_at=item.get("updated_at", ""),
                    pushed_at=item.get("pushed_at", ""),
                    is_fork=item.get("fork", False),
                    is_archived=item.get("archived", False),
                )
                repos.append(repo)

            if len(page_data) < per_page:
                break
            page += 1

        logger.info(f"Retrieved {len(repos)} repositories. Fetching language telemetry...")

        # Concurrently fetch language statistics per repository using ThreadPoolExecutor
        if repos:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [
                    executor.submit(self._fetch_languages_for_repo, repo)
                    for repo in repos
                    if not repo.is_fork  # Skip fork repo language calls to save quota
                ]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logger.warning(f"Error in parallel language fetch thread: {e}")

        logger.info(f"Successfully processed repository telemetry for {len(repos)} repos.")
        return repos
