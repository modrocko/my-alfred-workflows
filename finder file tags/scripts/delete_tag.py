import os
import sys
import json
import subprocess

tag_to_remove = sys.argv[1].strip()
if not tag_to_remove:
    sys.exit(0)

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")
title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit(0)

# Load file data
with open(db_path, "r") as f:
    data = json.load(f)

# Remove entries with matching tag
data = [entry for entry in data if entry.get("tag") != tag_to_remove]

# Save updated data
with open(db_path, "w") as f:
    json.dump(data, f, indent=2)

# Notify
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed tag: {tag_to_remove}" with title "{title}"'
])
