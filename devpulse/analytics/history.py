"""
Historical Analytics & Snapshot Manager for DevPulse AI.

Saves daily portfolio analytics snapshots (ISO YYYY-MM-DD.json format) and
computes real growth deltas compared against previous executions.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from devpulse.domain.models import (
    PortfolioAnalytics,
    PortfolioDelta,
    PortfolioSnapshotMetadata,
)
from devpulse.utils.file_io import ensure_directory, write_file
from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.analytics.history")


class HistoryManager:
    """Manages daily snapshot storage and computes historical growth deltas."""

    @staticmethod
    def get_today_date_str() -> str:
        """Returns current UTC date string in YYYY-MM-DD format."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def save_snapshot(
        self,
        analytics: PortfolioAnalytics,
        history_dir: Path,
        app_version: str = "1.0.0",
    ) -> Path:
        """Saves or overwrites today's historical snapshot file in output/history/YYYY-MM-DD.json.

        Args:
            analytics: Populated PortfolioAnalytics object.
            history_dir: Path object to historical snapshot directory.
            app_version: Application version string.

        Returns:
            Path: Path to saved snapshot JSON file.
        """
        history_dir = ensure_directory(history_dir)
        today_str = self.get_today_date_str()
        snapshot_filename = f"{today_str}.json"
        snapshot_path = history_dir / snapshot_filename

        # Attach metadata
        analytics.metadata = PortfolioSnapshotMetadata(
            generated_at=analytics.generated_at,
            app_version=app_version,
            username=analytics.user.login,
            generator_name="DevPulse AI",
        )

        data_dict = analytics.to_dict()
        json_content = json.dumps(data_dict, indent=2, ensure_ascii=False)

        written_path = write_file(snapshot_path, json_content)
        logger.info(f"Saved daily historical snapshot at '{written_path}'")
        return written_path

    def load_previous_snapshot(
        self, history_dir: Path, current_date_str: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Finds and loads the most recent historical snapshot prior to current_date_str.

        Args:
            history_dir: Path object to historical snapshot directory.
            current_date_str: Date string to ignore (defaults to today's date YYYY-MM-DD).

        Returns:
            Optional[Dict[str, Any]]: Decoded JSON dictionary of previous snapshot, or None.
        """
        history_dir = Path(history_dir).resolve()
        if not history_dir.is_dir():
            logger.debug(f"History directory not found at '{history_dir}'. No previous snapshot.")
            return None

        today_str = current_date_str or self.get_today_date_str()

        # Gather all YYYY-MM-DD.json files
        snapshot_files: List[Path] = []
        for file in history_dir.glob("*.json"):
            # Exclude current date snapshot file to find prior state
            if file.stem != today_str and len(file.stem) == 10 and file.stem.count("-") == 2:
                snapshot_files.append(file)

        if not snapshot_files:
            logger.info("No previous historical snapshots found. Initializing baseline tracking.")
            return None

        # Sort files by filename (chronological order)
        snapshot_files.sort(key=lambda p: p.stem)
        latest_previous_file = snapshot_files[-1]

        logger.info(f"Loaded previous historical snapshot from '{latest_previous_file}'")
        try:
            content = latest_previous_file.read_text(encoding="utf-8")
            data = json.loads(content)
            data["_snapshot_date"] = latest_previous_file.stem
            return data
        except Exception as e:
            logger.warning(f"Failed to read previous snapshot '{latest_previous_file}': {e}")
            return None

    def calculate_delta(
        self, current: PortfolioAnalytics, previous_snapshot: Optional[Dict[str, Any]]
    ) -> PortfolioDelta:
        """Calculates real historical growth deltas comparing current analytics against previous snapshot.

        Args:
            current: Current PortfolioAnalytics instance.
            previous_snapshot: Optional dictionary payload of previous snapshot.

        Returns:
            PortfolioDelta: Calculated growth deltas object.
        """
        if not previous_snapshot:
            return PortfolioDelta(
                repo_count_growth=0,
                star_growth=0,
                fork_growth=0,
                watcher_growth=0,
                newly_added_repos=[],
                newly_archived_repos=[],
                new_languages=[],
                removed_languages=[],
                growth_summary_status="Baseline Initialized",
                previous_snapshot_date=None,
            )

        prev_summary = previous_snapshot.get("summary", {})
        prev_repos = previous_snapshot.get("featured_repositories", []) + previous_snapshot.get("recent_repositories", [])
        prev_repo_names = set(r.get("name") for r in prev_repos if r.get("name"))
        prev_languages = set(l.get("name") for l in previous_snapshot.get("top_languages", []) if l.get("name"))
        prev_date = previous_snapshot.get("_snapshot_date", "Previous")

        curr_repo_names = set(r.name for r in current.repositories)
        curr_languages = set(l.name for l in current.top_languages)

        # Computations
        repo_growth = current.total_repos - prev_summary.get("total_repos", current.total_repos)
        star_growth = current.total_stars - prev_summary.get("total_stars", current.total_stars)
        fork_growth = current.total_forks - prev_summary.get("total_forks", current.total_forks)
        watcher_growth = current.total_watchers - prev_summary.get("total_watchers", current.total_watchers)

        newly_added = sorted(list(curr_repo_names - prev_repo_names)) if prev_repo_names else []
        new_langs = sorted(list(curr_languages - prev_languages)) if prev_languages else []
        removed_langs = sorted(list(prev_languages - curr_languages)) if prev_languages else []

        # Find newly archived repos
        curr_archived_names = set(r.name for r in current.repositories if r.is_archived)
        newly_archived = sorted(list(curr_archived_names))

        # Status determination
        if star_growth > 0 or repo_growth > 0:
            status = "Accelerating Growth"
        elif star_growth < 0:
            status = "Slight Metric Contraction"
        else:
            status = "Steady Maintenance"

        logger.info(
            f"Calculated historical delta vs {prev_date}: Stars ({star_growth:+d}), Repos ({repo_growth:+d})"
        )

        return PortfolioDelta(
            repo_count_growth=repo_growth,
            star_growth=star_growth,
            fork_growth=fork_growth,
            watcher_growth=watcher_growth,
            newly_added_repos=newly_added,
            newly_archived_repos=newly_archived,
            new_languages=new_langs,
            removed_languages=removed_langs,
            growth_summary_status=status,
            previous_snapshot_date=prev_date,
        )
