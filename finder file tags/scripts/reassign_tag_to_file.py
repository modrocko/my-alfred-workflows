import os
import sys
import json
import subprocess

# Get new tag from input
new_tag = sys.argv[1].strip().replace("!", "❗")

# Get metadata from environment
path = os.environ.get("path", "").strip()
old_tag = os.environ.get("old_tag", "").strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")
notif_title = os.environ["alfred_workflow_name"]

# Make sure data file exists
if not os.path.exists(db_path):
    print("Data file not found")
    sys.exit(1)

# Load data
with open(db_path, "r") as f:
    files = json.load(f)

# Update tags for the file
updated = []
changed = False

for item in files:
    if item.get("tag") == old_tag and path in item.get("paths", []):
        item["paths"].remove(path)
        changed = True
        if item["paths"]:
            updated.append(item)
        # Else: drop this tag if no more paths
    else:
        updated.append(item)

# Add new tag entry
if changed:
    found = False
    for item in updated:
        if item.get("tag") == new_tag:
            if path not in item["paths"]:
                item["paths"].append(path)
            found = True
            break
    if not found:
        updated.append({
            "tag": new_tag,
            "paths": [path]
        })

# Save file
with open(db_path, "w") as f:
    json.dump(updated, f, indent=2)

# Notify
if changed:
    print(f"✅ Reassigned tag '{old_tag}' → '{new_tag}'")
    subprocess.run([
        "osascript", "-e",
        f'display notification "File reassigned from \\"{old_tag}\\" to \\"{new_tag}\\"" with title "{notif_title}"'
    ])
else:
    print("❌ Tag not reassigned")
