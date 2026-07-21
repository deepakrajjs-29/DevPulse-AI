# DevPulse AI - Installation Guide

This document covers system requirements, setup instructions, dependency management, and verification steps for **DevPulse AI – GitHub Portfolio Assistant**.

---

## Prerequisites

- **Python Version**: Python 3.9 or higher (Python 3.10+ recommended).
- **Git**: Installed and configured on your path.
- **GitHub Account**: A valid GitHub account and optional Personal Access Token (PAT) for authenticated REST API requests.

---

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/DevPulse-AI/DevPulse-AI.git
cd "DevPulse-AI"
```

### 2. Create Virtual Environment (Recommended)
It is best practice to run DevPulse AI within an isolated Python virtual environment:

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux (Bash)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries specified in `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Core Dependencies Installed:
| Package | Minimum Version | Purpose |
| :--- | :--- | :--- |
| `requests` | `2.31.0` | High-performance HTTP REST client with retries |
| `python-dotenv` | `1.0.0` | Loads environment variables from `.env` |
| `Jinja2` | `3.1.2` | dynamic README markdown template engine |
| `PyYAML` | `6.0.1` | Application settings parser |

---

## Installation Sanity Check

Run the automated unit test suite to verify that your installation environment is configured properly:

```bash
python -m unittest discover -s tests
```

Expected output:
```text
......
----------------------------------------------------------------------
Ran 12 tests in 0.15s

OK
```
