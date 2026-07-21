# DevPulse AI – GitHub Portfolio Assistant

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%26%20Modular-brightgreen?style=for-the-badge)](docs/folder_structure.md)
[![Automation](https://img.shields.io/badge/DevPulse_AI-Automated_Daily-7057ff?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/devpulse_portfolio.yml)
[![Phase](https://img.shields.io/badge/Phase-2%20Automation%20Engine-orange?style=for-the-badge)](#)

**DevPulse AI** is an automated GitHub portfolio intelligence platform. It inspects developer profiles, calculates deep telemetry metrics (project health, repository growth, coding trends, developer activity, and strategic insights), generates structured JSON analytics payloads, and renders dynamic Markdown portfolio READMEs using Jinja2 templates.

---

## ⚡ Key Features

- **GitHub Actions Daily Automation**: Automated daily cron schedule (`0 0 * * *`) and `workflow_dispatch` manual triggers.
- **Pure Python Change Detector**: SHA-256 content hashing (`devpulse/automation/change_detector.py`) preventing unnecessary git commits when telemetry remains unchanged.
- **Concurrent GitHub REST API Client**: Multi-threaded parallel fetching of language statistics via `ThreadPoolExecutor` with retry strategy (`urllib3.util.Retry`) and rate-limit tracking.
- **Advanced Telemetry & Strategic Insights**:
  - 🩺 **Project Health**: Active vs archived repos, license coverage %, description coverage %, open issue counts.
  - 📈 **Repository Growth**: Account age in years, average stars/forks per repo, newest/oldest repository tracking.
  - 💻 **Coding Trends**: Primary technology trends, language diversity index, active language breakdown.
  - ⚡ **Developer Activity**: Velocity metrics (past 30 days updates/creates), most active repository identification.
  - 🧠 **Strategic Portfolio Insights**: Maturity level ("Established", "Growing", "Emerging"), strongest project identification, documentation completeness score.
- **Pluggable Exporters**: Decoupled JSON serializer and Jinja2 dynamic Markdown README exporter with custom formatting filters (`k_format`, ASCII `percentage_bar`, table sanitizers, date formatters).

---

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── devpulse_portfolio.yml  # GitHub Actions Daily Automation Workflow
├── config/
│   └── config.yaml                 # YAML application settings (limits, template paths, featured pins)
├── devpulse/
│   ├── domain/                     # Domain DTOs (UserProfile, Repository, Health, Growth, Trends)
│   ├── api/                        # Concurrent GitHub REST API client & exception hierarchy
│   ├── analytics/                  # Statistical calculator & telemetry aggregator
│   ├── automation/                 # SHA-256 change detector module
│   ├── exporters/                  # JSON & Markdown Jinja2 template builders
│   ├── services/                   # Service pipeline orchestrator
│   ├── config/                     # Environment & YAML settings manager
│   └── utils/                      # Centralized logging & safe file I/O
├── templates/
│   └── default_readme.md.j2        # Dynamic Jinja2 portfolio template
├── docs/                           # Documentation suite
│   ├── automation.md               # Automation architecture & change detector guide
│   ├── github_actions.md           # GitHub Actions setup & secrets configuration
│   ├── installation.md
│   ├── configuration.md
│   ├── folder_structure.md
│   └── usage.md
├── tests/                          # Automated unit test suite (15 passing tests)
├── output/                         # Target directory for generated artifacts
│   ├── analytics.json
│   └── README.md
├── main.py                         # Command line interface (CLI) entry point
├── requirements.txt                # Dependency pin manifest
└── README.md
```

---

## ⚡ Quick Start

### 1. Installation
```bash
# Clone the repository and navigate to root directory
cd "d:/Projects/DevPulse AI"

# Install required dependencies
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file from the provided template:
```bash
cp .env.example .env
```
Edit `.env` to supply your GitHub Personal Access Token and default username:
```ini
GITHUB_TOKEN=ghp_yourPersonalAccessTokenHere
GITHUB_USERNAME=octocat
```

### 3. Run Portfolio Engine
```bash
python main.py --username octocat
```

Upon execution, generated artifacts will be created in `output/`:
- `output/analytics.json`: Structured portfolio analytics telemetry.
- `output/README.md`: Dynamic Markdown README compiled from Jinja2 templates.

---

## 📖 Documentation Suite

Detailed guides are available in the [`docs/`](docs/) directory:
- [**Automation Guide**](docs/automation.md): Architecture of the SHA-256 change detector.
- [**GitHub Actions Guide**](docs/github_actions.md): Workflow configuration & secrets setup.
- [**Installation Guide**](docs/installation.md): Environment requirements and setup instructions.
- [**Configuration Guide**](docs/configuration.md): Environment variables and YAML schema reference.
- [**Folder Structure & Architecture**](docs/folder_structure.md): Deep-dive into module boundaries and design patterns.
- [**Usage Guide**](docs/usage.md): CLI options, template customization, and programmatic API usage.

---

## 🧪 Running Unit Tests

```bash
python -m unittest discover -s tests
```
