import datetime
import json
import os

today = str(datetime.date.today())

# Load daily log
if os.path.exists("data/daily_log.json"):
    with open("data/daily_log.json", "r") as f:
        daily_log = json.load(f)
else:
    daily_log = {}

# Add today's entry if not exists
if today not in daily_log:
    daily_log[today] = {
        "problems_solved": 0,
        "hours_studied": 0
    }

with open("data/daily_log.json", "w") as f:
    json.dump(daily_log, f, indent=4)

# Update metrics
with open("data/metrics.json", "r") as f:
    metrics = json.load(f)

metrics["current_streak"] += 1

with open("data/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Daily log updated.")
