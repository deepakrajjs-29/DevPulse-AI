"""
Domain Data Models (DTOs) for DevPulse AI.

Provides strongly-typed dataclasses representing GitHub entity models,
aggregated portfolio telemetry, project health, repository growth,
coding trends, developer activity, historical deltas, and strategic insights.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LanguageUsage:
    """Represents byte usage and calculated percentage for a programming language."""

    name: str
    bytes_count: int
    percentage: float


@dataclass
class Repository:
    """Represents a GitHub repository entity with core metrics and language details."""

    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stargazers_count: int
    forks_count: int
    watchers_count: int
    open_issues_count: int
    primary_language: Optional[str]
    languages: Dict[str, int] = field(default_factory=dict)
    topics: List[str] = field(default_factory=list)
    license_name: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""
    pushed_at: str = ""
    is_fork: bool = False
    is_archived: bool = False
    is_featured: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the repository entity to a clean dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "description": self.description or "",
            "html_url": self.html_url,
            "stargazers_count": self.stargazers_count,
            "forks_count": self.forks_count,
            "watchers_count": self.watchers_count,
            "open_issues_count": self.open_issues_count,
            "primary_language": self.primary_language or "N/A",
            "languages": self.languages,
            "topics": self.topics,
            "license_name": self.license_name or "N/A",
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "pushed_at": self.pushed_at,
            "is_fork": self.is_fork,
            "is_archived": self.is_archived,
            "is_featured": self.is_featured,
        }


@dataclass
class UserProfile:
    """Represents a GitHub developer profile."""

    login: str
    name: Optional[str]
    avatar_url: str
    html_url: str
    bio: Optional[str]
    company: Optional[str]
    location: Optional[str]
    blog: Optional[str]
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        """Converts the user profile entity to a clean dictionary."""
        return {
            "login": self.login,
            "name": self.name or self.login,
            "avatar_url": self.avatar_url,
            "html_url": self.html_url,
            "bio": self.bio or "",
            "company": self.company or "",
            "location": self.location or "",
            "blog": self.blog or "",
            "public_repos": self.public_repos,
            "public_gists": self.public_gists,
            "followers": self.followers,
            "following": self.following,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ProjectHealth:
    """Represents project health overview telemetry calculated from real repository metadata."""

    active_repos_count: int
    archived_repos_count: int
    license_coverage_pct: float
    description_coverage_pct: float
    total_open_issues: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active_repos_count": self.active_repos_count,
            "archived_repos_count": self.archived_repos_count,
            "license_coverage_pct": self.license_coverage_pct,
            "description_coverage_pct": self.description_coverage_pct,
            "total_open_issues": self.total_open_issues,
        }


@dataclass(frozen=True)
class RepositoryGrowth:
    """Represents repository metrics and portfolio growth over time."""

    total_repos: int
    newest_repo_name: str
    oldest_repo_name: str
    account_age_years: float
    avg_stars_per_repo: float
    avg_forks_per_repo: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_repos": self.total_repos,
            "newest_repo_name": self.newest_repo_name,
            "oldest_repo_name": self.oldest_repo_name,
            "account_age_years": self.account_age_years,
            "avg_stars_per_repo": self.avg_stars_per_repo,
            "avg_forks_per_repo": self.avg_forks_per_repo,
        }


@dataclass(frozen=True)
class CodingTrend:
    """Represents programming language diversity and dominant technology trends."""

    primary_trend_language: str
    language_diversity_score: int
    active_languages_count: int
    top_language_percentage: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_trend_language": self.primary_trend_language,
            "language_diversity_score": self.language_diversity_score,
            "active_languages_count": self.active_languages_count,
            "top_language_percentage": self.top_language_percentage,
        }


@dataclass(frozen=True)
class DeveloperActivity:
    """Represents recent development velocity and repository activity timestamps."""

    recently_updated_count: int
    recently_created_count: int
    most_active_repo_name: str
    latest_repo_name: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recently_updated_count": self.recently_updated_count,
            "recently_created_count": self.recently_created_count,
            "most_active_repo_name": self.most_active_repo_name,
            "latest_repo_name": self.latest_repo_name,
        }


@dataclass(frozen=True)
class PortfolioInsights:
    """Strategic AI & algorithmic observations calculated from repository analytics."""

    strongest_repo_name: str
    repo_needing_attention_name: str
    most_maintained_repo_name: str
    documentation_completeness_pct: float
    portfolio_maturity_level: str
    health_overview_status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strongest_repo_name": self.strongest_repo_name,
            "repo_needing_attention_name": self.repo_needing_attention_name,
            "most_maintained_repo_name": self.most_maintained_repo_name,
            "documentation_completeness_pct": self.documentation_completeness_pct,
            "portfolio_maturity_level": self.portfolio_maturity_level,
            "health_overview_status": self.health_overview_status,
        }


@dataclass(frozen=True)
class PortfolioSnapshotMetadata:
    """Metadata attached to historical analytics snapshots."""

    generated_at: str
    app_version: str
    username: str
    generator_name: str = "DevPulse AI"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "app_version": self.app_version,
            "username": self.username,
            "generator_name": self.generator_name,
        }


@dataclass(frozen=True)
class PortfolioDelta:
    """Represents real historical metric deltas compared against a previous snapshot."""

    repo_count_growth: int
    star_growth: int
    fork_growth: int
    watcher_growth: int
    newly_added_repos: List[str]
    newly_archived_repos: List[str]
    new_languages: List[str]
    removed_languages: List[str]
    growth_summary_status: str
    previous_snapshot_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo_count_growth": self.repo_count_growth,
            "star_growth": self.star_growth,
            "fork_growth": self.fork_growth,
            "watcher_growth": self.watcher_growth,
            "newly_added_repos": self.newly_added_repos,
            "newly_archived_repos": self.newly_archived_repos,
            "new_languages": self.new_languages,
            "removed_languages": self.removed_languages,
            "growth_summary_status": self.growth_summary_status,
            "previous_snapshot_date": self.previous_snapshot_date or "None",
        }


@dataclass
class PortfolioAnalytics:
    """Aggregated analytical telemetry for a developer's GitHub portfolio."""

    user: UserProfile
    repositories: List[Repository]
    total_repos: int
    total_stars: int
    total_forks: int
    total_watchers: int
    total_open_issues: int
    top_languages: List[LanguageUsage]
    featured_repos: List[Repository]
    recent_repos: List[Repository]
    project_health: Optional[ProjectHealth] = None
    repository_growth: Optional[RepositoryGrowth] = None
    coding_trend: Optional[CodingTrend] = None
    developer_activity: Optional[DeveloperActivity] = None
    portfolio_insights: Optional[PortfolioInsights] = None
    portfolio_delta: Optional[PortfolioDelta] = None
    metadata: Optional[PortfolioSnapshotMetadata] = None
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes analytics metrics into structured dictionary payload."""
        payload: Dict[str, Any] = {
            "user": self.user.to_dict(),
            "summary": {
                "total_repos": self.total_repos,
                "total_stars": self.total_stars,
                "total_forks": self.total_forks,
                "total_watchers": self.total_watchers,
                "total_open_issues": self.total_open_issues,
            },
            "top_languages": [
                {
                    "name": lang.name,
                    "bytes": lang.bytes_count,
                    "percentage": lang.percentage,
                }
                for lang in self.top_languages
            ],
            "featured_repositories": [repo.to_dict() for repo in self.featured_repos],
            "recent_repositories": [repo.to_dict() for repo in self.recent_repos],
            "generated_at": self.generated_at,
        }

        if self.metadata:
            payload["metadata"] = self.metadata.to_dict()
        if self.project_health:
            payload["project_health"] = self.project_health.to_dict()
        if self.repository_growth:
            payload["repository_growth"] = self.repository_growth.to_dict()
        if self.coding_trend:
            payload["coding_trend"] = self.coding_trend.to_dict()
        if self.developer_activity:
            payload["developer_activity"] = self.developer_activity.to_dict()
        if self.portfolio_insights:
            payload["portfolio_insights"] = self.portfolio_insights.to_dict()
        if self.portfolio_delta:
            payload["portfolio_delta"] = self.portfolio_delta.to_dict()

        return payload
