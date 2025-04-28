import os
import sys
import json
import subprocess

tag = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")

if not os.path.exists(db_path):
    sys.exit(0)

with open(db_path, "r") as f:
    bookmarks = json.load(f)

# Find the tag group
tag_entry = next((b for b in bookmarks if b.get("tag") == tag), None)

# Open all URLs under the tag
if tag_entry:
    for entry in tag_entry.get("urls", []):
        url = entry.get("url")
        if url:
            subprocess.run(["open", url])
