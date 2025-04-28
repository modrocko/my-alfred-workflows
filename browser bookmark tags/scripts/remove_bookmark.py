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

tag_removed = False

# Find the tag group
tag_entry = next((b for b in bookmarks if b.get("tag") == tag_to_remove), None)

if tag_entry:
    original_count = len(tag_entry["urls"])
    tag_entry["urls"] = [entry for entry in tag_entry["urls"] if entry.get("url") != url]
    if len(tag_entry["urls"]) != original_count:
        tag_removed = True

# Remove the tag group completely if no URLs left
bookmarks = [b for b in bookmarks if b.get("urls")]

# Save updated bookmarks
with open(db_path, "w") as f:
    json.dump(bookmarks, f, indent=2)

# Notify if tag was removed
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Bookmark removed from \\"{tag_to_remove}\\"" with title "{notif_title}"'
    ])
