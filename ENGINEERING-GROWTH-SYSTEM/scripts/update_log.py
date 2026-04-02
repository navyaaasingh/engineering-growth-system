"""
update_log.py
Appends today's entry to data/commit_log.txt and data/daily_log.json
"""

import json
from datetime import datetime, timezone

METRICS_FILE  = "data/metrics.json"
LOG_TXT_FILE  = "data/commit_log.txt"
DAILY_LOG     = "data/daily_log.json"


def main():
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    with open(METRICS_FILE) as f:
        metrics = json.load(f)

    streak  = metrics.get("current_streak", 0)
    commits = metrics.get("total_commits", 0)

    # Append to commit_log.txt
    with open(LOG_TXT_FILE, "a") as f:
        f.write(f"[{timestamp}] | commits: {commits} | streak: {streak} days\n")

    # Append to daily_log.json
    with open(DAILY_LOG) as f:
        daily = json.load(f)

    entry = {"date": today, "timestamp": timestamp, "commits": commits, "streak": streak}
    # Avoid duplicate entries for the same day
    daily["entries"] = [e for e in daily["entries"] if e["date"] != today]
    daily["entries"].append(entry)
    daily["entries"].sort(key=lambda x: x["date"], reverse=True)
    daily["last_updated"] = timestamp

    with open(DAILY_LOG, "w") as f:
        json.dump(daily, f, indent=2)

    print(f"✅ Log updated for {today}")


if __name__ == "__main__":
    main()
