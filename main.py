#!/usr/bin/env python3
"""
DevPulse AI - GitHub Portfolio Assistant.
Phase 2 Automation & Advanced Analytics Engine Entry Point.

Command Line Interface for executing portfolio analysis, stats extraction,
change detection, and dynamic README template generation.
"""

import argparse
import sys
from pathlib import Path

from devpulse.api.exceptions import DevPulseException
from devpulse.config.manager import ConfigManager
from devpulse.services.portfolio_service import PortfolioService
from devpulse.utils.logger import setup_logger


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments for DevPulse AI.

    Returns:
        argparse.Namespace: Parsed CLI options.
    """
    parser = argparse.ArgumentParser(
        description="DevPulse AI – Dynamic GitHub Portfolio Assistant (Phase 2 Automation Engine)"
    )
    parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="Target GitHub username to inspect (overrides GITHUB_USERNAME env var).",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to custom config.yaml settings file.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="Target output directory for generated analytics.json and README.md.",
    )
    parser.add_argument(
        "--check-changes",
        action="store_true",
        help="Runs SHA-256 change detection scan against existing output files.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose DEBUG level logging.",
    )
    return parser.parse_args()


def main() -> int:
    """CLI main entry point.

    Returns:
        int: System status exit code (0 = success, 1 = error).
    """
    args = parse_args()

    # Configure root logger
    log_level = "DEBUG" if args.verbose else "INFO"
    log_file = Path.cwd() / "logs" / "devpulse.log"
    logger = setup_logger(name="devpulse", log_level=log_level, log_file=log_file)

    logger.info("Initializing DevPulse AI Phase 2 Automation Engine...")

    try:
        # Load configuration
        config_path = Path(args.config) if args.config else None
        config_mgr = ConfigManager(config_path=config_path)

        if args.output_dir:
            config_mgr.output.directory = args.output_dir

        # Run portfolio service
        service = PortfolioService(config_manager=config_mgr)
        analytics, changed_files = service.run(
            username_override=args.username,
            check_changes_only=args.check_changes,
        )

        # Print success summary to stdout
        print("\n" + "=" * 65)
        print(" [DEVPULSE AI] PORTFOLIO ENGINE COMPLETED SUCCESSFULLY")
        print("=" * 65)
        print(f" Developer Profile : {analytics.user.name or analytics.user.login} (@{analytics.user.login})")
        print(f" Public Repos      : {analytics.total_repos}")
        print(f" Total Stars Earned: {analytics.total_stars}")
        print(f" Total Forks       : {analytics.total_forks}")
        print(f" Top Language      : {analytics.top_languages[0].name if analytics.top_languages else 'N/A'}")
        if analytics.portfolio_insights:
            print(f" Health Overview   : {analytics.portfolio_insights.health_overview_status}")
            print(f" Portfolio Maturity: {analytics.portfolio_insights.portfolio_maturity_level}")
        print(f" Output Location   : {config_mgr.get_output_directory().resolve()}")
        print(f"   |-- JSON Analytics: {config_mgr.get_analytics_path().name}")
        print(f"   |-- Markdown README: {config_mgr.get_readme_path().name}")
        print(f" Change Detection  : {len(changed_files)} file(s) modified")
        print("=" * 65 + "\n")

        return 0

    except DevPulseException as e:
        logger.error(f"DevPulse Application Error: {e}")
        print(f"\n[ERROR] Application Failure: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.critical(f"Unhandled unexpected system error: {e}", exc_info=True)
        print(f"\n[FATAL ERROR] An unexpected error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
