import os
import sys
import json
import subprocess

tag_to_remove = sys.argv[1].strip()
if not tag_to_remove:
    sys.exit(0)

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit(0)

# Load current bookmarks
with open(db_path, "r") as f:
    bookmarks = json.load(f)

# Remove the entire tag group
bookmarks = [b for b in bookmarks if b.get("tag") != tag_to_remove]

# Save updated bookmarks
with open(db_path, "w") as f:
    json.dump(bookmarks, f, indent=2)

# Show macOS notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed tag: {tag_to_remove}" with title "{title}"'
])
