import os
import sys
import json
import subprocess

# Get inputs
new_tag = sys.argv[1].strip().replace("!", "❗")
url = os.environ.get("url", "").strip()
old_tag = os.environ.get("old_tag", "").strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
notif_title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    print("Data file not found")
    sys.exit(1)

with open(db_path, "r") as f:
    bookmarks = json.load(f)

updated = []
tag_changed = False

for bm in bookmarks:
    if bm.get("url") == url:
        tags = bm.get("tags", [])
        if old_tag in tags:
            tags.remove(old_tag)
            if new_tag not in tags:
                tags.append(new_tag)
            bm["tags"] = tags
            tag_changed = True
    updated.append(bm)

if tag_changed:
    with open(db_path, "w") as f:
        json.dump(updated, f, indent=2)

    subprocess.run([
        "osascript", "-e",
        f'display notification "Reassigned tag to \\"{new_tag}\\"" with title "{notif_title}"'
    ])