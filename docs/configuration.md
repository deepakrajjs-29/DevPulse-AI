# DevPulse AI - Configuration Guide

DevPulse AI follows the 12-Factor App methodology, decoupling credentials and secrets (managed via `.env`) from application portfolio settings (managed via `config/config.yaml`).

---

## 1. Environment Variables (`.env`)

Environment variables are loaded automatically from the `.env` file in the root directory via `python-dotenv`.

Copy `.env.example` to create your local `.env`:
```bash
cp .env.example .env
```

### Environment Parameters Reference

| Variable Name | Required | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `GITHUB_TOKEN` | Optional | `None` | GitHub Personal Access Token (PAT). Increases rate limit from 60 req/hr to 5,000 req/hr. |
| `GITHUB_USERNAME` | Optional* | `""` | Target GitHub username to analyze (*Can also be passed via CLI `--username`). |
| `LOG_LEVEL` | Optional | `INFO` | Verbosity level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |

> [!TIP]
> **Generating a GitHub Personal Access Token (PAT):**
> 1. Go to GitHub Settings -> **Developer Settings** -> **Personal Access Tokens** -> **Tokens (classic)**.
> 2. Click **Generate new token**.
> 3. Select scope `public_repo` or `read:user`.
> 4. Copy the generated token string into your `.env` file (`GITHUB_TOKEN=ghp_xxxx`).

---

## 2. YAML Settings (`config/config.yaml`)

Application limits, template paths, and repository filtering options are configured cleanly in `config/config.yaml`.

```yaml
app:
  name: "DevPulse AI"
  version: "1.0.0"
  description: "GitHub Portfolio Assistant - Phase 1 Core Engine"

portfolio:
  # Maximum top languages to include in analytics and README
  top_languages_count: 6

  # Maximum featured repositories to display
  featured_repos_count: 4

  # Maximum recent repositories to display
  recent_repos_count: 6

  # Repository filtering parameters
  include_forks: false
  include_archived: false

  # Optional explicit list of repository names to feature (if empty, ranks by star count)
  featured_repo_names:
    - "my-starred-project"
    - "awesome-library"

templates:
  # Path to Jinja2 README template
  readme_template: "templates/default_readme.md.j2"

output:
  # Destination directory for generated artifacts
  directory: "output"
  analytics_file: "analytics.json"
  readme_file: "README.md"

api:
  # Network HTTP request timeout (seconds)
  timeout: 10
  # Max worker threads for parallel language detail fetching
  max_workers: 5
  # Remaining quota threshold to trigger log warnings
  min_rate_limit_warning: 10
```
