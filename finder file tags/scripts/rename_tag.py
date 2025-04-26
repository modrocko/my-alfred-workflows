import json
import os
import sys
import subprocess

new_tag = sys.argv[1].strip().replace("!", "❗")
old_tag = os.getenv("old_tag")

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")
title = os.environ["alfred_workflow_name"]

# Load data
with open(db_path, "r") as f:
    data = json.load(f)

# Update tags
for entry in data:
    if entry.get("tag") == old_tag:
        entry["tag"] = new_tag

# Save updated data
with open(db_path, "w") as f:
    json.dump(data, f, indent=2)

# Notify
subprocess.run([
    "osascript", "-e",
    f'display notification "Tag renamed from {old_tag} to {new_tag}." with title "{title}"'
])
