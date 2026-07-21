# DevPulse AI - Usage Guide

This guide describes how to run DevPulse AI via the Command Line Interface (CLI) and how to integrate it programmatically into Python scripts.

---

## 💻 Command Line Interface (CLI)

The main entry point for running DevPulse AI is `main.py`.

### Basic Usage

Analyze a specific user (overriding `.env`):
```bash
python main.py --username octocat
```

Run using environment variables configured in `.env`:
```bash
python main.py
```

### CLI Command Flags

```bash
python main.py [OPTIONS]
```

| Flag | Short | Type | Description |
| :--- | :--- | :--- | :--- |
| `--username` | `-u` | `string` | Target GitHub username to analyze. |
| `--config` | `-c` | `string` | Path to a custom YAML configuration file. |
| `--output-dir` | `-o` | `string` | Custom output directory path for generated files. |
| `--check-changes` | | `flag` | Performs SHA-256 change detection scan against existing output files. |
| `--verbose` | `-v` | `flag` | Enables verbose `DEBUG` level logging output to console. |
| `--help` | `-h` | `flag` | Displays help message and CLI options summary. |

### CLI Execution Examples

#### 1. Verbose Inspection with Change Detection
```bash
python main.py --username octocat --check-changes --verbose
```

#### 2. Custom Output Location and Configuration
```bash
python main.py --username octocat --config config/config.yaml --output-dir dist/
```

---

## 🎨 Customizing the Jinja2 README Template

DevPulse AI uses Jinja2 to render dynamic markdown portfolios.

The template file is located at `templates/default_readme.md.j2`.

### Available Context Variables in Jinja2

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `user` | `UserProfile` | User attributes (`name`, `login`, `avatar_url`, `bio`, `followers`, `blog`, etc.). |
| `summary` | `dict` | Telemetry totals (`total_repos`, `total_stars`, `total_forks`, `total_watchers`, `total_open_issues`). |
| `project_health` | `ProjectHealth` | Health indicators (`active_repos_count`, `license_coverage_pct`, `description_coverage_pct`). |
| `repository_growth` | `RepositoryGrowth` | Growth statistics (`account_age_years`, `avg_stars_per_repo`, `newest_repo_name`). |
| `coding_trend` | `CodingTrend` | Technology trends (`primary_trend_language`, `language_diversity_score`). |
| `developer_activity` | `DeveloperActivity` | Velocity metrics (`recently_updated_count`, `most_active_repo_name`). |
| `portfolio_insights` | `PortfolioInsights` | Strategic observations (`strongest_repo_name`, `portfolio_maturity_level`, `health_overview_status`). |
| `top_languages` | `List[LanguageUsage]` | List of language statistics (`name`, `bytes_count`, `percentage`). |
| `featured_repos` | `List[Repository]` | List of selected featured repository entities. |
| `recent_repos` | `List[Repository]` | List of recent repository entities. |
| `generated_at` | `str` | ISO 8601 UTC timestamp of execution. |

---

## 🐍 Programmatic Python Integration

You can import and use DevPulse AI programmatically inside your own Python code:

```python
from devpulse.config.manager import ConfigManager
from devpulse.services.portfolio_service import PortfolioService

# 1. Initialize Configuration
config_mgr = ConfigManager()

# 2. Instantiate Service Pipeline
service = PortfolioService(config_manager=config_mgr)

# 3. Execute Analysis & Change Detection
analytics, changed_files = service.run(username_override="octocat")

# Access calculated Phase 2 metrics directly
print(f"User: {analytics.user.name}")
print(f"Health Status: {analytics.portfolio_insights.health_overview_status}")
print(f"Maturity Level: {analytics.portfolio_insights.portfolio_maturity_level}")
print(f"Changed Output Files: {len(changed_files)}")
```
