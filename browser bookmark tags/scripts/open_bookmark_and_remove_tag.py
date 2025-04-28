import os
import json
import subprocess

url = os.environ.get("url", "").strip()
tag = os.environ.get("tag", "").strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
notif_title = os.environ["alfred_workflow_name"]

if not url or not tag:
    print("❌ Missing url or tag")
    exit()

# 🌐 Open the tab first
subprocess.run(["open", url])

tag_removed = False
bookmarks = []

if os.path.exists(db_path):
    with open(db_path, "r") as f:
        bookmarks = json.load(f)

    # Find the tag group
    tag_entry = next((b for b in bookmarks if b.get("tag") == tag), None)

    if tag_entry:
        original_count = len(tag_entry["urls"])
        tag_entry["urls"] = [entry for entry in tag_entry["urls"] if entry.get("url") != url]
        if len(tag_entry["urls"]) != original_count:
            tag_removed = True

    # Remove the entire tag if it has no URLs left
    bookmarks = [b for b in bookmarks if b.get("urls")]

    with open(db_path, "w") as f:
        json.dump(bookmarks, f, indent=2)

# ✅ Notification
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Removed URL from tag \\"{tag}\\"" with title "{notif_title}"'
    ])
