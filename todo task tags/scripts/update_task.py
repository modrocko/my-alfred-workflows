import os
import sys
import json

# Parse input: tag||old_task||new_task
try:
    tag, old_task, new_task = map(str.strip, sys.argv[1].split("||", 2))
    new_task = new_task.replace("!", "❗")  # Handle special char
except:
    sys.exit(0)

# Path to tasks.json
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

if not os.path.exists(db_path):
    sys.exit(0)

# Load existing tasks
with open(db_path, "r") as f:
    data = json.load(f)

# Find matching task under tag & update it
for entry in data:
    if entry.get("tag") == tag:
        tasks = entry.get("tasks", [])
        if old_task in tasks:
            tasks[tasks.index(old_task)] = new_task
        break

# Save changes
with open(db_path, "w") as f:
    json.dump(data, f, indent=2)
