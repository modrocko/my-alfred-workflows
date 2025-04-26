import json
import os
import sys
import subprocess

# Get tags
new_tag = sys.argv[1].strip().replace("!", "❗")
old_tag = os.getenv("old_tag")

# Get paths
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")
title = os.environ["alfred_workflow_name"]

# Load task data
with open(db_path, "r") as f:
    tasks = json.load(f)

# Find existing entries
old_entry = None
new_entry = None
for entry in tasks:
    if entry.get("tag") == old_tag:
        old_entry = entry
    if entry.get("tag") == new_tag:
        new_entry = entry

# Merge or rename
if old_entry:
    if new_entry:
        # Append old tasks to existing new tag
        new_entry["tasks"].extend(old_entry["tasks"])
        tasks.remove(old_entry)
    else:
        # Just rename old tag
        old_entry["tag"] = new_tag

# Save updated data
with open(db_path, "w") as f:
    json.dump(tasks, f, indent=2)

# Notify user
subprocess.run([
    "osascript", "-e",
    f'display notification "Tag renamed from {old_tag} to {new_tag}." with title "{title}"'
])
