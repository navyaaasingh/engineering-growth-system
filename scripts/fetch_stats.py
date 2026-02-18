import json

with open("data/metrics.json", "r") as f:
    metrics = json.load(f)

print("Current Metrics:")
print(metrics)
