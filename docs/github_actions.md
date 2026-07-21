# DevPulse AI - GitHub Actions & Secrets Setup Guide

This guide explains how to deploy **DevPulse AI** to run automatically in your GitHub repository using GitHub Actions workflows.

---

## ⚡ Workflow Configuration (`.github/workflows/devpulse_portfolio.yml`)

DevPulse AI includes a production-grade GitHub Actions workflow stored at `.github/workflows/devpulse_portfolio.yml`.

### Triggers
1. **Scheduled Execution**: Automatically executes once per day at 00:00 UTC using cron syntax (`cron: '0 0 * * *'`).
2. **Manual Dispatch**: Can be triggered manually on demand via the **Actions** tab in GitHub.

---

## 🔑 GitHub Secrets & Permissions Setup

DevPulse AI relies on the automatic built-in `secrets.GITHUB_TOKEN` provided by GitHub Actions. **No third-party tokens or credentials are required.**

### 1. Enable Repository Workflow Write Permissions

For GitHub Actions to push updated `README.md` and `analytics.json` files back to your repository, you must grant **Read and Write permissions**:

1. Open your repository on GitHub.
2. Go to **Settings** -> **Actions** -> **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Check **Allow GitHub Actions to create and approve pull requests** (if applicable).
6. Click **Save**.

```text
Workflow permissions
(•) Read and write permissions
    Workflows have read and write permissions in the repository for all scopes.
```

---

## 🚀 Manual Execution & Testing Workflow

To manually test your GitHub Actions workflow:

1. Navigate to the **Actions** tab on your GitHub repository.
2. Select **DevPulse AI Daily Portfolio Automation** from the left sidebar.
3. Click the **Run workflow** dropdown button.
4. Click **Run workflow**.

---

## 🛠️ Troubleshooting & Common Issues

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `Permission to repo denied to github-actions[bot]` | Missing write permissions in repository settings. | Enable **Read and write permissions** under **Settings -> Actions -> General -> Workflow permissions**. |
| `Rate limit exceeded (HTTP 403)` | Operating in unauthenticated mode or exceeding 5,000 req/hr limit. | Ensure `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` is supplied in workflow environment variables. |
| Workflow loops continuously | Git commits triggering new workflow runs. | The workflow uses `[skip ci]` tag in commit messages to automatically bypass workflow triggers. |
