# DevPulse AI - Automation & Change Detection Guide

DevPulse AI includes a production-grade automation layer designed to execute portfolio analysis on a scheduled basis, detect content changes using cryptographic hashing, and maintain dynamic GitHub portfolios automatically.

---

## 🏛️ Automation Architecture Overview

```text
┌──────────────────────────────────────────────────────────┐
│             GitHub Actions Workflow (Cron / Dispatch)    │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│            DevPulse AI Core Engine (main.py)             │
├────────────────────────────┬─────────────────────────────┤
│ 1. GitHub API Fetcher      │ Pulls profile & repos       │
│ 2. Analytics Calculator    │ Computes health & trends    │
│ 3. Jinja2 Exporters        │ Renders JSON & README.md    │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│          SHA-256 Change Detector (Pure Python)           │
│         devpulse/automation/change_detector.py           │
├──────────────────────────────────────────────────────────┤
│ • Computes SHA-256 hashes of generated artifacts         │
│ • Compares new content against existing disk files       │
│ • Identifies modified output files                       │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│       Idempotent Git Committer (GitHub Actions Bot)      │
├──────────────────────────────────────────────────────────┤
│ • If modified: git commit -m "chore(portfolio)..." & push│
│ • If clean: Log "No changes detected" & exit 0           │
└──────────────────────────────────────────────────────────┘
```

---

## 🔒 Pure Python Change Detection (`ChangeDetector`)

Change detection is powered by `devpulse/automation/change_detector.py`. It uses 256-bit Secure Hash Algorithm (SHA-256) cryptographic digests to compare newly generated strings against existing files on disk before committing changes.

### Key Benefits
1. **Idempotency**: Running DevPulse AI multiple times per day produces zero extra commits if repository telemetry has not changed.
2. **Prevent Infinite CI Loops**: Automated commits use the `[skip ci]` message tag to prevent triggering cascading workflow builds.
3. **Bandwidth & Rate Limit Hygiene**: Prevents git churn and unnecessary repository object bloat.

### SHA-256 Hashing Implementation
```python
from devpulse.automation.change_detector import ChangeDetector

detector = ChangeDetector()

# Check single file change
is_modified = detector.has_changed("output/README.md", rendered_content)

# Scan multiple files
changed_files = detector.detect_changes({
    path_json: new_json_str,
    path_readme: new_readme_str,
})
```
