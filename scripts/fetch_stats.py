"""
fetch_stats.py
Fetches GitHub commit stats and writes them to data/metrics.json
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "navyaaasingh")  # fallback hardcoded
GITHUB_TOKEN    = os.environ.get("GITHUB_TOKEN", "")
METRICS_FILE    = "data/metrics.json"


def fetch_recent_commits():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public?per_page=100"
    req = urllib.request.Request(url)
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    req.add_header("User-Agent", "engineering-growth-system")

    try:
        with urllib.request.urlopen(req) as resp:
            events = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"⚠️  GitHub API error: {e.code} {e.reason}. Using cached data.")
        return [], 0
    except Exception as e:
        print(f"⚠️  Network error: {e}. Using cached data.")
        return [], 0

    push_days = set()
    total_commits = 0
    for event in events:
        if event.get("type") == "PushEvent":
            day = event["created_at"][:10]
            push_days.add(day)
            total_commits += len(event["payload"].get("commits", []))

    return sorted(push_days, reverse=True), total_commits


def calculate_streak(active_days):
    if not active_days:
        return 0
    streak = 0
    today = datetime.now(timezone.utc).date()
    for i in range(len(active_days)):
        expected = str(today - timedelta(days=i))
        if active_days[i] == expected:
            streak += 1
        else:
            break
    return streak


def main():
    try:
        with open(METRICS_FILE) as f:
            metrics = json.load(f)
    except Exception:
        metrics = {
            "last_updated": "",
            "total_commits": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "active_days": [],
            "weekly": {"commits": 0, "lines_added": 0, "lines_removed": 0}
        }

    active_days, total_commits = fetch_recent_commits()

    if not active_days and total_commits == 0:
        print("⚠️  No data from API, keeping cached values.")
        active_days = metrics.get("active_days", [])
        total_commits = metrics.get("total_commits", 0)

    current_streak = calculate_streak(active_days)
    longest_streak = max(metrics.get("longest_streak", 0), current_streak)

    #metrics.update({
        "last_updated":   datetime.now(timezone.utc).isoformat(),
        "total_commits":  total_commits,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "active_days":    active_days[:30],
    })

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"✅ Metrics updated — streak: {current_streak} days, commits: {total_commits}")


#if __name__ == "__main__":
#    main()
