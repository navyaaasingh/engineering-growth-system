import datetime
import json
import os
import random
import time

today = str(datetime.date.today())

# Load daily log
if os.path.exists("data/daily_log.json"):
    with open("data/daily_log.json", "r") as f:
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

with open("data/daily_log.json", "w") as f:
    json.dump(daily_log, f, indent=4)

print(f"Generated {num_updates} updates today.")