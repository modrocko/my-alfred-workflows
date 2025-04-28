import os
import sys
import json
import subprocess

tag_to_remove = sys.argv[1].strip()
if not tag_to_remove:
    sys.exit(0)

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit(0)

# Load current emails
with open(db_path, "r") as f:
    emails = json.load(f)

# Remove entire tag group
emails = [tag_entry for tag_entry in emails if tag_entry.get("tag") != tag_to_remove]

# Save updated data
with open(db_path, "w") as f:
    json.dump(emails, f, indent=2)

# Show notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed tag: {tag_to_remove}" with title "{title}"'
])
