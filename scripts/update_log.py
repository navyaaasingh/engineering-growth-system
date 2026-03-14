import datetime
import json
import os
import random
import subprocess
import sys


def run_command(cmd, error_msg, allow_fail=False):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and not allow_fail:
        print(f"ERROR - {error_msg}:\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


today = str(datetime.date.today())

os.makedirs("data", exist_ok=True)

log_path = "data/daily_log.json"

# Load JSON safely
if os.path.exists(log_path):
    try:
        with open(log_path, "r") as f:
            daily_log = json.load(f)
    except json.JSONDecodeError:
        daily_log = {}
else:
    daily_log = {}

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

print("\nCommitting and pushing to GitHub...")

# Sync repository first
run_command("git pull --rebase origin main", "Failed to pull latest changes")

run_command("git add data/daily_log.json", "Failed to stage file")

commit_msg = f"chore: log {num_updates} updates for {today}"

# Allow commit to fail if nothing changed
run_command(f'git commit -m "{commit_msg}"', "Commit skipped", allow_fail=True)

run_command("git push origin main", "Failed to push to remote")

print(f"Finished GitHub update.")