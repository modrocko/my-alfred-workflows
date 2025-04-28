import os
import sys
import json
import subprocess

# Input is something like: message_id||tag
parts = sys.argv[1].split("||")
if len(parts) != 2:
    sys.exit()

message_id = parts[0].strip()
tag_to_remove = parts[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit()

with open(db_path, "r") as f:
    emails = json.load(f)

tag_removed = False

# Find the tag group
for tag_entry in emails:
    if tag_entry.get("tag") == tag_to_remove:
        original_count = len(tag_entry["emails"])
        tag_entry["emails"] = [entry for entry in tag_entry["emails"] if entry.get("id") != message_id]
        if len(tag_entry["emails"]) != original_count:
            tag_removed = True
        break

# Remove the tag group if it has no emails left
emails = [b for b in emails if b.get("emails")]

with open(db_path, "w") as f:
    json.dump(emails, f, indent=2)

# ✅ Notification if tag was removed
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Email removed from \\"{tag_to_remove}\\"" with title "{title}"'
    ])
