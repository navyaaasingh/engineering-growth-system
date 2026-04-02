# 🚀 Engineering Growth System

Automatically tracks and commits your GitHub engineering activity every day.

## Structure

```
.github/workflows/
  daily-update.yml      # GitHub Actions workflow (runs daily)
  persist-credentials   # Git credential config for local use

data/
  commit_log.txt        # Append-only log of every run
  daily_log.json        # Structured daily entries
  metrics.json          # Streak, commit counts, active days
  weekly_summary.md     # Human-readable weekly report

scripts/
  fetch_stats.py        # Pulls commit data from GitHub API
  update_log.py         # Writes to commit_log.txt & daily_log.json
  generate_summary.py   # Renders weekly_summary.md
```

## Setup

### 1. Add your GitHub username
Edit `scripts/fetch_stats.py` and set `GITHUB_USERNAME`.

### 2. Add a secret (for private repo access)
Go to **Settings → Secrets → Actions** and add:
- `GITHUB_TOKEN` — a Personal Access Token with `repo` scope

### 3. Push and enable Actions
GitHub Actions will run automatically at midnight UTC every day.
You can also trigger it manually from the **Actions** tab.

## Running locally

```bash
export GITHUB_USERNAME="your-username"
export GITHUB_TOKEN="your-token"

python scripts/fetch_stats.py
python scripts/update_log.py
python scripts/generate_summary.py
```
