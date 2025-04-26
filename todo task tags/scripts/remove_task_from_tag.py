import os
import sys
import json
import subprocess

# Split input
try:
    tag, task = map(str.strip, sys.argv[1].split("||", 1))
except:
    sys.exit(0)

# Paths
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

# Exit if file missing
if not os.path.exists(db_path):
    sys.exit(0)

# Load data
with open(db_path, "r") as f:
    data = json.load(f)

# Remove task from matching tag group
updated = []
for entry in data:
    if entry["tag"] == tag:
        tasks = [t for t in entry["tasks"] if t != task]
        if tasks:
            updated.append({ "tag": tag, "tasks": tasks })
        # else: don't include empty tag group
    else:
        updated.append(entry)

# Save
with open(db_path, "w") as f:
    json.dump(updated, f, indent=2)

# Notify
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed: {task}" with title "Task Removed"'
])
