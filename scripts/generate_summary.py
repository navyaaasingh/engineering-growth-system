import json

with open("data/daily_log.json", "r") as f:
    daily_log = json.load(f)

summary = "# Weekly Summary\n\n"

last_7_days = list(daily_log.keys())[-7:]

for day in last_7_days:
    summary += f"- {day}\n"

with open("data/weekly_summary.md", "w") as f:
    f.write(summary)

print("Weekly summary generated.")
