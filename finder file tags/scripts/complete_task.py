import os
import sys
import json

try:
    tag, task = map(str.strip, sys.argv[1].split("||", 1))
except:
    sys.exit(0)

# File path
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

if not os.path.exists(db_path):
    sys.exit(0)

# Load data
with open(db_path, "r") as f:
    data = json.load(f)

# Update task
for entry in data:
    if entry.get("tag") == tag:
        tasks = entry.get("tasks", [])
        if task in tasks:
            idx = tasks.index(task)
            tasks[idx] = f"✅ {task}"
        break

# Save it
with open(db_path, "w") as f:
    json.dump(data, f, indent=2)
