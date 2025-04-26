import os
import sys
import json
import subprocess

# Input is something like: path||tag
parts = sys.argv[1].split("||")
if len(parts) != 2:
    sys.exit()

path = parts[0].strip()
tag_to_remove = parts[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")
title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit()

with open(db_path, "r") as f:
    files = json.load(f)

updated = []
tag_removed = False

for item in files:
    if path in item.get("paths", []):
        if tag_to_remove == item.get("tag"):
            item["paths"].remove(path)
            tag_removed = True
        if item["paths"]:
            updated.append(item)
    else:
        updated.append(item)

with open(db_path, "w") as f:
    json.dump(updated, f, indent=2)

# ✅ Notification if tag was removed
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "File removed from \\"{tag_to_remove}\\"" with title "{title}"'
    ])
