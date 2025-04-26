import os
import sys
import json
import subprocess

# Get tag to remove
tag_to_remove = sys.argv[1].strip()
if not tag_to_remove:
    sys.exit(0)

# Paths
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")
title = os.environ["alfred_workflow_name"]

# Make sure tasks.json exists
if not os.path.exists(db_path):
    sys.exit(0)

# Load tasks
with open(db_path, "r") as f:
    tasks = json.load(f)

# Remove all entries with the given tag
updated = [entry for entry in tasks if entry.get("tag") != tag_to_remove]

# Save updated list
with open(db_path, "w") as f:
    json.dump(updated, f, indent=2)

# Notify user
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed tag: {tag_to_remove}" with title "{title}"'
])
