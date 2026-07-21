# DevPulse AI - Folder Structure & Architecture Walkthrough

DevPulse AI is architected using modular, object-oriented design principles. Business logic, data models, network communications, automation, and file outputs are decoupled into distinct layers.

---

## 📁 Folder Structure Map

```text
d:/Projects/DevPulse AI/
├── .github/
│   └── workflows/
│       └── devpulse_portfolio.yml  # Daily GitHub Actions Automation Workflow
├── config/
│   └── config.yaml                 # YAML application configuration settings
├── devpulse/
│   ├── __init__.py                 # Package root initialization
│   ├── domain/                     # Core Domain Models & Abstractions
│   │   ├── __init__.py
│   │   ├── models.py               # Domain DTOs (UserProfile, Repository, ProjectHealth, Growth, Trends)
│   │   └── interfaces.py           # Protocol contracts (APIClientProtocol, ExporterProtocol)
│   ├── api/                        # Network & GitHub API Layer
│   │   ├── __init__.py
│   │   ├── client.py               # Concurrent GitHub REST API Client
│   │   └── exceptions.py           # Domain Exception Taxonomy
│   ├── analytics/                  # Statistical Calculation Engine
│   │   ├── __init__.py
│   │   └── calculator.py           # Metrics, language ratios, health, growth, & insights aggregator
│   ├── automation/                 # Pure Python Automation & Change Detection
│   │   ├── __init__.py
│   │   └── change_detector.py      # SHA-256 content change detector
│   ├── exporters/                  # Output Generation Layer
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract BaseExporter interface
│   │   ├── json_exporter.py        # Structured JSON serializer
│   │   └── markdown_exporter.py    # Jinja2 dynamic README exporter & custom filters
│   ├── services/                   # Application Service Orchestration
│   │   ├── __init__.py
│   │   └── portfolio_service.py    # End-to-end telemetry pipeline runner
│   ├── config/                     # Configuration Manager
│   │   ├── __init__.py
│   │   └── manager.py              # Typed .env and YAML parser
│   └── utils/                      # Common Utilities
│       ├── __init__.py
│       ├── logger.py               # Dual-target structured logging
│       └── file_io.py              # Directory and safe file IO helpers
├── templates/
│   └── default_readme.md.j2        # Dynamic Jinja2 portfolio Markdown template
├── output/                         # Target directory for generated output artifacts
│   ├── analytics.json              # Exported raw analytics payload
│   └── README.md                   # Rendered dynamic markdown portfolio README
├── docs/                           # Documentation suite
│   ├── automation.md               # Automation & change detector guide
│   ├── github_actions.md           # GitHub Actions setup & secrets configuration
│   ├── installation.md
│   ├── configuration.md
│   ├── folder_structure.md
│   └── usage.md
├── tests/                          # Automated unit test suite
│   ├── test_automation.py          # SHA-256 change detector tests
│   ├── test_config.py
│   ├── test_api_client.py
│   ├── test_analytics.py           # Phase 1 & Phase 2 analytics tests
│   ├── test_exporters.py
│   └── test_service.py
├── .env.example                    # Environment settings template
├── .gitignore                      # Git exclusions list
├── requirements.txt                # Dependency manifest
├── main.py                         # CLI entry point script
└── README.md                       # Project overview README
```

---

## 🏛️ Architectural Layer Breakdown

### 1. Domain Layer (`devpulse/domain/`)
- Contains pure Python dataclasses (`UserProfile`, `Repository`, `LanguageUsage`, `PortfolioAnalytics`, `ProjectHealth`, `RepositoryGrowth`, `CodingTrend`, `DeveloperActivity`, `PortfolioInsights`) with zero external network or I/O dependencies.

### 2. Automation Layer (`devpulse/automation/`)
- `ChangeDetector`: Pure Python SHA-256 cryptographic hasher used to scan generated content against existing disk files to enforce idempotency and avoid unnecessary git commits.

### 3. API Layer (`devpulse/api/`)
- `GitHubClient`: Manages HTTP connection pooling, exponential backoff retries, custom headers, rate-limit tracking, auto-pagination, and multi-threaded parallel language detail fetching via `ThreadPoolExecutor`.

### 4. Analytics Layer (`devpulse/analytics/`)
- `AnalyticsCalculator`: Calculates language distribution ratios, project health scores, repository growth metrics, coding trends, developer activity, and strategic insights derived strictly from GitHub REST API data.

### 5. Exporters Layer (`devpulse/exporters/`)
- `JSONExporter`: Serializes portfolio analytics into structured JSON payloads.
- `MarkdownExporter`: Renders Jinja2 Markdown templates (`templates/default_readme.md.j2`) using registered custom filters (`k_format`, ASCII `percentage_bar`, `sanitize_markdown`, `format_date`).
