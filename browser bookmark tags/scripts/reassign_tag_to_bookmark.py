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

tag_changed = False

# Step 1: Find old tag group
old_tag_entry = next((b for b in bookmarks if b.get("tag") == old_tag), None)

# Step 2: Find or create new tag group
new_tag_entry = next((b for b in bookmarks if b.get("tag") == new_tag), None)
if not new_tag_entry:
    new_tag_entry = {"tag": new_tag, "urls": []}
    bookmarks.append(new_tag_entry)

# Step 3: Move URL from old to new
if old_tag_entry:
    for entry in old_tag_entry.get("urls", []):
        if entry.get("url") == url:
            new_tag_entry["urls"].append(entry)
            old_tag_entry["urls"].remove(entry)
            tag_changed = True
            break

# Step 4: Remove old tag group if empty
bookmarks = [b for b in bookmarks if b.get("urls")]

# Step 5: Save if changed
if tag_changed:
    with open(db_path, "w") as f:
        json.dump(bookmarks, f, indent=2)

    subprocess.run([
        "osascript", "-e",
        f'display notification "Reassigned tag to \\"{new_tag}\\"" with title "{notif_title}"'
    ])
