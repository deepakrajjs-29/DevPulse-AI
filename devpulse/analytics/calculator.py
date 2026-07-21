"""
Analytics Calculator for DevPulse AI.

Processes raw repository models and user profiles into structured portfolio analytics,
calculating language distributions, aggregate metrics, featured highlights, project health,
repository growth, coding trends, developer activity, and portfolio insights.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from devpulse.config.manager import PortfolioConfig
from devpulse.domain.models import (
    CodingTrend,
    DeveloperActivity,
    LanguageUsage,
    PortfolioAnalytics,
    PortfolioInsights,
    ProjectHealth,
    Repository,
    RepositoryGrowth,
    UserProfile,
)
from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.analytics")


class AnalyticsCalculator:
    """Calculates deep telemetry metrics, language usage ratios, health indicators, and strategic insights."""

    def __init__(self, config: Optional[PortfolioConfig] = None):
        """Initializes calculator with optional portfolio rules configuration.

        Args:
            config: Optional PortfolioConfig instance.
        """
        self.config = config or PortfolioConfig()

    def calculate(
        self, user: UserProfile, repositories: List[Repository]
    ) -> PortfolioAnalytics:
        """Processes developer profile and repositories to produce a complete PortfolioAnalytics payload.

        Args:
            user: Developer profile entity.
            repositories: List of repository domain entities.

        Returns:
            PortfolioAnalytics: Aggregated domain telemetry payload.
        """
        logger.info(
            f"Calculating portfolio analytics for user '{user.login}' across {len(repositories)} repositories."
        )

        # Filter repositories based on settings
        filtered_repos = self._filter_repositories(repositories)

        # Aggregate Phase 1 core metrics
        total_repos = len(repositories)
        total_stars = sum(repo.stargazers_count for repo in repositories)
        total_forks = sum(repo.forks_count for repo in repositories)
        total_watchers = sum(repo.watchers_count for repo in repositories)
        total_open_issues = sum(repo.open_issues_count for repo in repositories)

        # Calculate language usage
        top_languages = self._calculate_language_usage(
            repositories=filtered_repos,
            top_count=self.config.top_languages_count,
        )

        # Identify featured repositories
        featured_repos = self._select_featured_repositories(
            repositories=filtered_repos,
            explicit_pins=self.config.featured_repo_names,
            max_count=self.config.featured_repos_count,
        )

        # Identify recent repositories
        recent_repos = self._select_recent_repositories(
            repositories=filtered_repos,
            max_count=self.config.recent_repos_count,
        )

        # Phase 2 Analytics Calculations
        project_health = self._calculate_project_health(repositories)
        repository_growth = self._calculate_repository_growth(user, repositories)
        coding_trend = self._calculate_coding_trends(top_languages, filtered_repos)
        developer_activity = self._calculate_developer_activity(filtered_repos)
        portfolio_insights = self._calculate_portfolio_insights(
            user, repositories, project_health, coding_trend
        )

        logger.info(
            f"Phase 2 Analytics complete: Health Status '{portfolio_insights.health_overview_status}', "
            f"Maturity '{portfolio_insights.portfolio_maturity_level}'."
        )

        return PortfolioAnalytics(
            user=user,
            repositories=repositories,
            total_repos=total_repos,
            total_stars=total_stars,
            total_forks=total_forks,
            total_watchers=total_watchers,
            total_open_issues=total_open_issues,
            top_languages=top_languages,
            featured_repos=featured_repos,
            recent_repos=recent_repos,
            project_health=project_health,
            repository_growth=repository_growth,
            coding_trend=coding_trend,
            developer_activity=developer_activity,
            portfolio_insights=portfolio_insights,
        )

    def _filter_repositories(self, repositories: List[Repository]) -> List[Repository]:
        """Filters repositories according to fork and archive settings."""
        filtered: List[Repository] = []
        for repo in repositories:
            if repo.is_fork and not self.config.include_forks:
                continue
            if repo.is_archived and not self.config.include_archived:
                continue
            filtered.append(repo)
        return filtered

    def _calculate_language_usage(
        self, repositories: List[Repository], top_count: int
    ) -> List[LanguageUsage]:
        """Calculates language bytes distribution and percentage breakdown across repositories."""
        language_bytes: Dict[str, int] = {}

        for repo in repositories:
            if repo.languages:
                for lang_name, bytes_cnt in repo.languages.items():
                    language_bytes[lang_name] = language_bytes.get(lang_name, 0) + bytes_cnt
            elif repo.primary_language and repo.primary_language != "N/A":
                language_bytes[repo.primary_language] = (
                    language_bytes.get(repo.primary_language, 0) + 1000
                )

        total_bytes = sum(language_bytes.values())
        if total_bytes == 0:
            return []

        usage_list: List[LanguageUsage] = []
        for lang_name, bytes_cnt in language_bytes.items():
            pct = round((bytes_cnt / total_bytes) * 100, 2)
            usage_list.append(
                LanguageUsage(
                    name=lang_name,
                    bytes_count=bytes_cnt,
                    percentage=pct,
                )
            )

        usage_list.sort(key=lambda lang: lang.bytes_count, reverse=True)
        return usage_list[:top_count]

    def _select_featured_repositories(
        self,
        repositories: List[Repository],
        explicit_pins: List[str],
        max_count: int,
    ) -> List[Repository]:
        """Selects featured repositories based on explicit pins or engagement metrics."""
        featured: List[Repository] = []

        if explicit_pins:
            lower_pins = [name.lower() for name in explicit_pins]
            for repo in repositories:
                if repo.name.lower() in lower_pins:
                    repo.is_featured = True
                    featured.append(repo)

        remaining_slots = max_count - len(featured)
        if remaining_slots > 0:
            candidates = [r for r in repositories if r not in featured]
            candidates.sort(
                key=lambda r: (r.stargazers_count, r.forks_count, r.watchers_count),
                reverse=True,
            )
            for repo in candidates[:remaining_slots]:
                repo.is_featured = True
                featured.append(repo)

        return featured

    def _select_recent_repositories(
        self, repositories: List[Repository], max_count: int
    ) -> List[Repository]:
        """Selects recent repositories based on updated_at date timestamp."""
        sorted_repos = sorted(
            repositories,
            key=lambda r: r.updated_at or r.pushed_at or "",
            reverse=True,
        )
        return sorted_repos[:max_count]

    def _calculate_project_health(self, repositories: List[Repository]) -> ProjectHealth:
        """Calculates project health indicators from repository license, description, and archive status."""
        total = len(repositories)
        if total == 0:
            return ProjectHealth(0, 0, 0.0, 0.0, 0)

        active_cnt = sum(1 for r in repositories if not r.is_archived)
        archived_cnt = sum(1 for r in repositories if r.is_archived)
        licensed_cnt = sum(1 for r in repositories if r.license_name and r.license_name != "N/A")
        described_cnt = sum(1 for r in repositories if r.description and r.description.strip())
        total_open_issues = sum(r.open_issues_count for r in repositories)

        license_pct = round((licensed_cnt / total) * 100, 1)
        desc_pct = round((described_cnt / total) * 100, 1)

        return ProjectHealth(
            active_repos_count=active_cnt,
            archived_repos_count=archived_cnt,
            license_coverage_pct=license_pct,
            description_coverage_pct=desc_pct,
            total_open_issues=total_open_issues,
        )

    def _calculate_repository_growth(
        self, user: UserProfile, repositories: List[Repository]
    ) -> RepositoryGrowth:
        """Calculates repository growth, account age in years, and average engagement statistics."""
        total = len(repositories)

        # Calculate account age in years
        account_age_years = 0.0
        if user.created_at:
            try:
                created_dt = datetime.fromisoformat(user.created_at.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                diff_days = (now - created_dt).days
                account_age_years = round(diff_days / 365.25, 1)
            except Exception:
                account_age_years = 0.0

        if total == 0:
            return RepositoryGrowth(0, "N/A", "N/A", account_age_years, 0.0, 0.0)

        # Sort by creation date to find oldest and newest
        created_sorted = sorted(
            [r for r in repositories if r.created_at],
            key=lambda r: r.created_at,
        )

        oldest_name = created_sorted[0].name if created_sorted else "N/A"
        newest_name = created_sorted[-1].name if created_sorted else "N/A"

        avg_stars = round(sum(r.stargazers_count for r in repositories) / total, 1)
        avg_forks = round(sum(r.forks_count for r in repositories) / total, 1)

        return RepositoryGrowth(
            total_repos=total,
            newest_repo_name=newest_name,
            oldest_repo_name=oldest_name,
            account_age_years=account_age_years,
            avg_stars_per_repo=avg_stars,
            avg_forks_per_repo=avg_forks,
        )

    def _calculate_coding_trends(
        self, top_languages: List[LanguageUsage], repositories: List[Repository]
    ) -> CodingTrend:
        """Calculates primary technology trend and language diversity score."""
        if not top_languages:
            return CodingTrend("N/A", 0, 0, 0.0)

        primary_lang = top_languages[0].name
        top_pct = top_languages[0].percentage

        # Count all distinct active languages across repos
        distinct_langs = set()
        for r in repositories:
            if r.languages:
                distinct_langs.update(r.languages.keys())
            elif r.primary_language and r.primary_language != "N/A":
                distinct_langs.add(r.primary_language)

        diversity_score = len(distinct_langs)

        return CodingTrend(
            primary_trend_language=primary_lang,
            language_diversity_score=diversity_score,
            active_languages_count=diversity_score,
            top_language_percentage=top_pct,
        )

    def _calculate_developer_activity(
        self, repositories: List[Repository]
    ) -> DeveloperActivity:
        """Calculates recent repository update velocity based on UTC timestamps."""
        if not repositories:
            return DeveloperActivity(0, 0, "N/A", "N/A")

        now = datetime.now(timezone.utc)
        recently_updated = 0
        recently_created = 0

        for r in repositories:
            # Check updated_at (within past 30 days)
            if r.updated_at or r.pushed_at:
                date_str = r.updated_at or r.pushed_at
                try:
                    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    if (now - dt).days <= 30:
                        recently_updated += 1
                except Exception:
                    pass

            # Check created_at (within past 30 days)
            if r.created_at:
                try:
                    dt = datetime.fromisoformat(r.created_at.replace("Z", "+00:00"))
                    if (now - dt).days <= 30:
                        recently_created += 1
                except Exception:
                    pass

        # Sort by engagement for most active repo
        most_active_repo = max(
            repositories,
            key=lambda r: (r.stargazers_count, r.forks_count, r.open_issues_count),
        )

        # Sort by updated date for latest repo
        latest_updated_repo = max(
            repositories,
            key=lambda r: r.updated_at or r.pushed_at or "",
        )

        return DeveloperActivity(
            recently_updated_count=recently_updated,
            recently_created_count=recently_created,
            most_active_repo_name=most_active_repo.name,
            latest_repo_name=latest_updated_repo.name,
        )

    def _calculate_portfolio_insights(
        self,
        user: UserProfile,
        repositories: List[Repository],
        health: ProjectHealth,
        trends: CodingTrend,
    ) -> PortfolioInsights:
        """Derives strategic observations regarding portfolio maturity, documentation quality, and repository health."""
        if not repositories:
            return PortfolioInsights("N/A", "N/A", "N/A", 0.0, "Emerging", "Needs Telemetry")

        # Strongest repo by engagement
        strongest_repo = max(repositories, key=lambda r: (r.stargazers_count, r.forks_count))

        # Repo needing attention (e.g. highest open issues or missing description)
        needing_attn = max(repositories, key=lambda r: (r.open_issues_count, not bool(r.description)))

        # Most maintained repo
        most_maintained = max(repositories, key=lambda r: r.updated_at or r.pushed_at or "")

        # Documentation completeness score (% with description & license)
        doc_completeness = round(
            (health.license_coverage_pct + health.description_coverage_pct) / 2.0, 1
        )

        # Portfolio maturity level
        if len(repositories) >= 10 and health.active_repos_count >= 5:
            maturity = "Established"
        elif len(repositories) >= 3:
            maturity = "Growing"
        else:
            maturity = "Emerging"

        # Overall health status string
        if doc_completeness >= 80.0:
            health_status = "Optimal"
        elif doc_completeness >= 50.0:
            health_status = "Healthy"
        else:
            health_status = "Needs Improvement"

        return PortfolioInsights(
            strongest_repo_name=strongest_repo.name,
            repo_needing_attention_name=needing_attn.name,
            most_maintained_repo_name=most_maintained.name,
            documentation_completeness_pct=doc_completeness,
            portfolio_maturity_level=maturity,
            health_overview_status=health_status,
        )
