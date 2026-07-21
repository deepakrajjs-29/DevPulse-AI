<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=220&section=header&text=DevPulse%20AI&fontSize=60&fontColor=00f0ff&animation=fadeIn&fontAlignY=38&desc=GitHub%20Portfolio%20Intelligence%20Engine&descAlignY=58&descSize=18" width="100%"/>

<br/>

<a href="https://python.org">
  <img src="https://img.shields.io/badge/Python-3.9%2B-00f0ff?style=for-the-badge&logo=python&logoColor=white&labelColor=0f0c29" />
</a>
<a href="docs/folder_structure.md">
  <img src="https://img.shields.io/badge/Architecture-Clean%20%26%20Modular-b967ff?style=for-the-badge&labelColor=0f0c29" />
</a>
<a href=".github/workflows/devpulse_portfolio.yml">
  <img src="https://img.shields.io/badge/DevPulse_AI-Automated_Daily-7057ff?style=for-the-badge&logo=githubactions&logoColor=white&labelColor=0f0c29" />
</a>
<a href="#">
  <img src="https://img.shields.io/badge/Phase-2%20Automation%20Engine-ff6ec7?style=for-the-badge&labelColor=0f0c29" />
</a>

<br/><br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=2800&pause=900&color=00F0FF&center=true&vCenter=true&width=780&lines=Inspecting+GitHub+profiles+in+real-time...;Calculating+deep+telemetry+metrics...;Generating+strategic+portfolio+insights...;Rendering+dynamic+Markdown+READMEs...;Zero+noise.+Zero+manual+edits.+Pure+signal." alt="Typing SVG" />

</div>

<br/>

<p align="center">
<b>DevPulse AI</b> is an automated GitHub portfolio intelligence platform. It inspects developer profiles, calculates deep telemetry &mdash; project health, repository growth, coding trends, developer activity, strategic insights &mdash; generates structured JSON analytics payloads, and renders dynamic Markdown portfolio READMEs using Jinja2 templates.
</p>

<div align="center">

![divider](https://capsule-render.vercel.app/api?type=rect&color=0:0f0c29,100:302b63&height=3&width=1000)

</div>

<br/>

## ⚡ Key Features

<table>
<tr>
<td width="50%" valign="top">

### 🔁 Automation Core
- **GitHub Actions Daily Automation** — cron `0 0 * * *` + manual `workflow_dispatch` triggers
- **Pure Python Change Detector** — SHA-256 content hashing (`devpulse/automation/change_detector.py`) skips redundant commits
- **Concurrent GitHub REST API Client** — multi-threaded language stats via `ThreadPoolExecutor`, retry strategy (`urllib3.util.Retry`), live rate-limit tracking

</td>
<td width="50%" valign="top">

### 🧠 Telemetry & Insights
- 🩺 **Project Health** — active/archived split, license & description coverage %, open issues
- 📈 **Repository Growth** — account age, avg stars/forks, newest/oldest repo
- 💻 **Coding Trends** — primary tech trends, language diversity index
- ⚡ **Developer Activity** — 30-day velocity, most active repo
- 🎯 **Strategic Insights** — maturity level, strongest project, doc completeness score

</td>
</tr>
</table>

<div align="center">

![divider](https://capsule-render.vercel.app/api?type=rect&color=0:302b63,100:0f0c29&height=3&width=1000)

</div>

## 🛰️ Pipeline

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#302b63','primaryTextColor':'#00f0ff','primaryBorderColor':'#00f0ff','lineColor':'#b967ff','secondaryColor':'#24243e','tertiaryColor':'#0f0c29'}}}%%
flowchart LR
    A["🔑 GitHub Token"] --> B["🌐 Concurrent API Client"]
    B --> C["📦 Domain DTOs"]
    C --> D["📊 Analytics Aggregator"]
    D --> E["🧮 SHA-256 Change Detector"]
    E -- "changed" --> F["🗂️ JSON Exporter"]
    E -- "changed" --> G["📝 Jinja2 Markdown Exporter"]
    E -- "unchanged" --> H["⏭️ Skip Commit"]
    F --> I["output/analytics.json"]
    G --> J["output/README.md"]
```

<br/>

## 📁 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── devpulse_portfolio.yml  # Daily automation workflow
├── config/
│   └── config.yaml                 # Limits, template paths, featured pins
├── devpulse/
│   ├── domain/                     # UserProfile, Repository, Health, Growth, Trends
│   ├── api/                        # Concurrent GitHub REST client + exception hierarchy
│   ├── analytics/                  # Statistical calculator & telemetry aggregator
│   ├── automation/                 # SHA-256 change detector
│   ├── exporters/                  # JSON & Jinja2 Markdown builders
│   ├── services/                   # Pipeline orchestrator
│   ├── config/                     # Env & YAML settings manager
│   └── utils/                      # Logging & safe file I/O
├── templates/
│   └── default_readme.md.j2        # Dynamic Jinja2 portfolio template
├── docs/                           # automation · github_actions · installation · configuration · folder_structure · usage
├── tests/                          # 15 passing unit tests
├── output/
│   ├── analytics.json
│   └── README.md
├── main.py                         # CLI entry point
└── requirements.txt
```

<div align="center">

![divider](https://capsule-render.vercel.app/api?type=rect&color=0:0f0c29,100:302b63&height=3&width=1000)

</div>

## 🚀 Quick Start

**1 · Install**
```bash
cd "d:/Projects/DevPulse AI"
pip install -r requirements.txt
```

**2 · Configure**
```bash
cp .env.example .env
```
```ini
GITHUB_TOKEN=ghp_yourPersonalAccessTokenHere
GITHUB_USERNAME=octocat
```

**3 · Run**
```bash
python main.py --username octocat
```

Generated artifacts land in `output/`:

| File | Description |
|---|---|
| `output/analytics.json` | Structured portfolio analytics telemetry |
| `output/README.md` | Dynamic Markdown README compiled from Jinja2 templates |

<br/>

## 📖 Documentation Suite

| Guide | Covers |
|---|---|
| [Automation](docs/automation.md) | SHA-256 change detector architecture |
| [GitHub Actions](docs/github_actions.md) | Workflow configuration & secrets |
| [Installation](docs/installation.md) | Environment requirements & setup |
| [Configuration](docs/configuration.md) | Env vars & YAML schema reference |
| [Folder Structure](docs/folder_structure.md) | Module boundaries & design patterns |
| [Usage](docs/usage.md) | CLI options, templating, API usage |

## 🧪 Testing

```bash
python -m unittest discover -s tests
```

<div align="center">

![divider](https://capsule-render.vercel.app/api?type=rect&color=0:302b63,100:0f0c29&height=3&width=1000)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer"/>

<sub>Built with 🩶 for developers who'd rather let telemetry write the README.</sub>

</div>
