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
updated = []

if os.path.exists(db_path):
    with open(db_path, "r") as f:
        bookmarks = json.load(f)

    for bm in bookmarks:
        if bm["url"] == url and tag in bm.get("tags", []):
            bm["tags"].remove(tag)
            tag_removed = True
            if bm["tags"]:
                updated.append(bm)
            # else: don't re-add
        else:
            updated.append(bm)

    with open(db_path, "w") as f:
        json.dump(updated, f, indent=2)

# ✅ Notification
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Removed tag \\"{tag}\\"" with title "{notif_title}"'
    ])
