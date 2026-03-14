import datetime
import json
import os
import random
import subprocess
import sys


def run_command(cmd, error_msg):
    """Run a shell command and exit on failure."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR - {error_msg}:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


today = str(datetime.date.today())

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Load daily log
log_path = "data/daily_log.json"
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        daily_log = json.load(f)
else:
    daily_log = {}

# Generate random number of updates (2–10)
num_updates = random.randint(2, 10)

if today not in daily_log:
    daily_log[today] = []

for i in range(num_updates):
    entry = {
        "update_number": i + 1,
        "timestamp": str(datetime.datetime.now())
    }
    daily_log[today].append(entry)

with open(log_path, "w") as f:
    json.dump(daily_log, f, indent=4)

print(f"Generated {num_updates} updates for {today}.")

# --- GitHub automation ---
print("\nCommitting and pushing to GitHub...")

run_command("git add data/daily_log.json", "Failed to stage file")

commit_msg = f"chore: log {num_updates} updates for {today}"
run_command(f'git commit -m "{commit_msg}"', "Failed to commit")

run_command("git push", "Failed to push to remote")

print(f"Successfully committed and pushed: '{commit_msg}'")