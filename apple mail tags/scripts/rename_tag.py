import json
import os
import sys
import subprocess

new_tag = sys.argv[1].strip().replace("!", "❗")
old_tag = os.getenv("old_tag")
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

# Load data
with open(db_path, "r") as f:
    emails = json.load(f)

# Find and rename the tag group
for tag_entry in emails:
    if tag_entry.get("tag") == old_tag:
        tag_entry["tag"] = new_tag
        break

# Save updated data
with open(db_path, "w") as f:
    json.dump(emails, f, indent=2)

# ✅ Notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Tag renamed from {old_tag} to {new_tag}." with title "{title}"'
])
