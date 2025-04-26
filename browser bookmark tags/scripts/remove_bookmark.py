import os
import sys
import json
import subprocess

# Input: url||tag
parts = sys.argv[1].split("||")
if len(parts) != 2:
    sys.exit()

url = parts[0].strip()
tag_to_remove = parts[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
notif_title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit()

with open(db_path, "r") as f:
    bookmarks = json.load(f)

# Remove tag & remove entry if no tags remain
updated = []
tag_removed = False

for bm in bookmarks:
    if bm.get("url") == url:
        tags = bm.get("tags", [])
        if tag_to_remove in tags:
            tags.remove(tag_to_remove)
            tag_removed = True
        if tags:
            bm["tags"] = tags
            updated.append(bm)
        # else: do not re-add bookmark (it's tagless)
    else:
        updated.append(bm)

with open(db_path, "w") as f:
    json.dump(updated, f, indent=2)

# Notify if tag was removed
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Bookmark removed from \\"{tag_to_remove}\\"" with title "{notif_title}"'
    ])