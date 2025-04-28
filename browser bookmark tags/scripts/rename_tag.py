import json
import os
import sys
import subprocess

# Get values
new_tag = sys.argv[1].strip().replace("!", "❗")
old_tag = os.getenv("old_tag", "").strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
title = os.environ["alfred_workflow_name"]

# Load data
if not os.path.exists(db_path):
    sys.exit(0)

with open(db_path, "r") as f:
    bookmarks = json.load(f)

# Find the tag entry
for bm in bookmarks:
    if bm.get("tag") == old_tag:
        bm["tag"] = new_tag

# Save updated data
with open(db_path, "w") as f:
    json.dump(bookmarks, f, indent=2)

# Show notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Tag renamed from {old_tag} to {new_tag}." with title "{title}"'
])
